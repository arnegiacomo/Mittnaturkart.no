from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from ..database import get_db
from ..models import User as UserModel
from ..schemas import User, UserCreate, Token
from ..auth import (
    create_access_token,
    exchange_code_for_token,
    get_user_info,
    get_current_user
)
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login-url")
def get_login_url():
    redirect_uri = f"{settings.frontend_url}/auth/callback"
    return {
        "url": f"{settings.keycloak_authorization_url}?"
               f"client_id={settings.keycloak_client_id}&"
               f"redirect_uri={redirect_uri}&"
               f"response_type=code&"
               f"scope=openid email profile"
    }

@router.post("/callback", response_model=Token)
async def auth_callback(
    code: str = Query(...),
    db: Session = Depends(get_db)
):
    redirect_uri = f"{settings.frontend_url}/auth/callback"

    logger.info(f"Auth callback initiated - Code: {code}")
    logger.info(f"Redirect URI: {redirect_uri}")
    logger.info(f"Keycloak token URL: {settings.keycloak_token_url}")

    try:
        keycloak_tokens = await exchange_code_for_token(code, redirect_uri)
        logger.info(f"Successfully exchanged code for tokens")
    except Exception as e:
        logger.error(f"Failed to exchange code: {str(e)}")
        raise

    keycloak_access_token = keycloak_tokens["access_token"]

    user_info = await get_user_info(keycloak_access_token)
    logger.info(f"User info from Keycloak: {user_info}")

    keycloak_id = user_info["sub"]
    email = user_info.get("email")
    name = user_info.get("username", email)

    if not email:
        logger.error(f"Email not provided by Keycloak for sub={keycloak_id}")
        raise HTTPException(status_code=400, detail="Email not provided by identity provider")

    user = db.query(UserModel).filter(UserModel.keycloak_id == keycloak_id).first()

    if user:
        logger.info(f"Existing user login: id={user.id}, email={email}, keycloak_id={keycloak_id}")
        user.email = email
        user.name = name
        db.commit()
        db.refresh(user)
    else:
        user = UserModel(
            keycloak_id=keycloak_id,
            email=email,
            name=name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"New user created: id={user.id}, email={email}, keycloak_id={keycloak_id}")

    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "username": user.name}
    )
    logger.info(f"JWT token issued for user: id={user.id}, email={user.email}, username={user.name}")

    expires_in_seconds = settings.access_token_expire_days * 24 * 60 * 60

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in_seconds
    }

@router.get("/logout-url")
def get_logout_url():
    return {
        "url": f"{settings.keycloak_logout_url}?"
               f"client_id={settings.keycloak_client_id}&"
               f"post_logout_redirect_uri={settings.frontend_url}"
    }

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    logger.info(f"User profile accessed: id={current_user.id}, email={current_user.email}")
    return current_user
