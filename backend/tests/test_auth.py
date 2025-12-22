import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import jwt, JWTError
from app.auth import create_access_token, decode_access_token
from app.config import settings


class TestJWTCreation:
    def test_create_token_with_valid_data(self):
        user_id = uuid4()
        data = {"sub": str(user_id), "email": "test@example.com", "username": "testuser"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contains_required_claims(self):
        user_id = uuid4()
        data = {"sub": str(user_id), "email": "test@example.com"}
        token = create_access_token(data)

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        assert "sub" in payload
        assert "email" in payload
        assert "exp" in payload
        assert "iat" in payload
        assert "nbf" in payload
        assert "jti" in payload
        assert "iss" in payload

        assert payload["sub"] == str(user_id)
        assert payload["email"] == "test@example.com"
        assert payload["iss"] == settings.jwt_issuer

    def test_token_expiration_is_correct(self):
        data = {"sub": str(uuid4()), "email": "test@example.com"}
        before = datetime.now(timezone.utc)
        token = create_access_token(data)
        after = datetime.now(timezone.utc)

        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected_min = (before + timedelta(days=settings.access_token_expire_days)).replace(microsecond=0)
        expected_max = (after + timedelta(days=settings.access_token_expire_days)).replace(microsecond=0) + timedelta(seconds=1)

        assert expected_min <= exp_time <= expected_max

    def test_jti_is_unique(self):
        data = {"sub": str(uuid4()), "email": "test@example.com"}
        token1 = create_access_token(data)
        token2 = create_access_token(data)

        payload1 = jwt.decode(token1, settings.secret_key, algorithms=[settings.algorithm])
        payload2 = jwt.decode(token2, settings.secret_key, algorithms=[settings.algorithm])

        assert payload1["jti"] != payload2["jti"]


class TestJWTValidation:
    def test_decode_valid_token(self):
        user_id = uuid4()
        data = {"sub": str(user_id), "email": "test@example.com"}
        token = create_access_token(data)

        token_data = decode_access_token(token)

        assert token_data is not None
        assert token_data.user_id == user_id
        assert token_data.email == "test@example.com"

    def test_decode_token_with_invalid_signature(self):
        user_id = uuid4()
        data = {"sub": str(user_id), "email": "test@example.com"}
        token = create_access_token(data)

        tampered_token = token[:-10] + "tampered123"
        token_data = decode_access_token(tampered_token)

        assert token_data is None

    def test_decode_token_with_wrong_secret(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=7)

        payload = {
            "sub": str(user_id),
            "email": "test@example.com",
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        wrong_token = jwt.encode(payload, "wrong_secret_key", algorithm=settings.algorithm)
        token_data = decode_access_token(wrong_token)

        assert token_data is None

    def test_decode_expired_token(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        expired = now - timedelta(days=1)

        payload = {
            "sub": str(user_id),
            "email": "test@example.com",
            "exp": expired,
            "iat": now - timedelta(days=8),
            "nbf": now - timedelta(days=8),
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        expired_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(expired_token)

        assert token_data is None

    def test_decode_token_with_wrong_issuer(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=7)

        payload = {
            "sub": str(user_id),
            "email": "test@example.com",
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid4()),
            "iss": "wrong-issuer"
        }

        wrong_issuer_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(wrong_issuer_token)

        assert token_data is None

    def test_decode_token_missing_sub(self):
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=7)

        payload = {
            "email": "test@example.com",
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(token)

        assert token_data is None

    def test_decode_token_missing_email(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=7)

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(token)

        assert token_data is None

    def test_decode_token_with_invalid_uuid(self):
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=7)

        payload = {
            "sub": "not-a-valid-uuid",
            "email": "test@example.com",
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(token)

        assert token_data is None

    def test_decode_malformed_token(self):
        token_data = decode_access_token("not.a.valid.token")
        assert token_data is None

    def test_decode_empty_token(self):
        token_data = decode_access_token("")
        assert token_data is None

    def test_nbf_claim_validation(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=1)

        payload = {
            "sub": str(user_id),
            "email": "test@example.com",
            "exp": now + timedelta(days=7),
            "iat": now,
            "nbf": future,
            "jti": str(uuid4()),
            "iss": settings.jwt_issuer
        }

        future_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        token_data = decode_access_token(future_token)

        assert token_data is None
