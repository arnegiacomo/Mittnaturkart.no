from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import httpx

from .config import settings
from .database import get_db
from .models import User as UserModel
from .schemas import TokenData

def get_security():
    if settings.disable_auth:
        return HTTPBearer(auto_error=False)
    return HTTPBearer()

security = get_security()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=settings.access_token_expire_days)
    to_encode.update({
        "exp": expire,
        "iat": now,
        "nbf": now,
        "jti": str(uuid4()),
        "iss": settings.jwt_issuer
    })
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    import logging
    logger = logging.getLogger(__name__)

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_iss": True},
            issuer=settings.jwt_issuer
        )
        logger.info(f"JWT payload decoded: {payload}")
        user_id_str: str = payload.get("sub")
        email: str = payload.get("email")
        logger.info(f"Extracted from payload - user_id_str: {user_id_str}, email: {email}")
        if user_id_str is None or email is None:
            logger.error(f"Missing user_id or email in token payload. user_id_str: {user_id_str}, email: {email}")
            return None
        user_id = UUID(user_id_str)
        return TokenData(user_id=user_id, email=email)
    except JWTError as e:
        logger.error(f"JWT decode error: {type(e).__name__}: {str(e)}")
        return None

async def exchange_code_for_token(code: str, redirect_uri: str) -> dict:
    import logging
    logger = logging.getLogger(__name__)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.keycloak_token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": settings.keycloak_client_id,
                "client_secret": settings.keycloak_client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code != 200:
            logger.error(f"Keycloak token exchange failed - Status: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            raise HTTPException(status_code=400, detail="Failed to exchange authorization code")
        return response.json()

async def get_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.keycloak_userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")
        return response.json()

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> UserModel:
    import logging
    logger = logging.getLogger(__name__)

    # Test mode: bypass authentication and return/create a test user
    if settings.disable_auth:
        logger.info("Auth disabled - using test user")
        test_user = db.query(UserModel).filter(UserModel.email == "test@example.com").first()
        if not test_user:
            test_user = UserModel(
                keycloak_id="test-user-id",
                email="test@example.com",
                name="Test User"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
        return test_user

    token = credentials.credentials
    logger.info(f"Validating token: {token[:20]}...")

    token_data = decode_access_token(token)

    if token_data is None:
        logger.error("Token decode failed - token_data is None")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"Token decoded successfully - user_id: {token_data.user_id}, email: {token_data.email}")

    user = db.query(UserModel).filter(UserModel.id == token_data.user_id).first()
    if user is None:
        logger.error(f"User not found in database - user_id: {token_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"User authenticated successfully - id: {user.id}, email: {user.email}")
    return user

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[UserModel]:
    if credentials is None:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
