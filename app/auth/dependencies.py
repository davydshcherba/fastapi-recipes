from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.auth_handler import decode_jwt

security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    payload = decode_jwt(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return payload["user_id"]
