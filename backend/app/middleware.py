from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .logging_context import set_sub, clear_sub
from .auth import decode_access_token

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        clear_sub()

        auth_header = request.headers.get("authorization")
        if not auth_header:
            return await call_next(request)

        try:
            scheme, credentials = auth_header.split()
        except ValueError:
            return await call_next(request)

        if scheme.lower() != "bearer":
            return await call_next(request)

        try:
            token_data = decode_access_token(credentials)
            if token_data:
                set_sub(str(token_data.user_id))
        except Exception:
            pass

        response = await call_next(request)
        return response
