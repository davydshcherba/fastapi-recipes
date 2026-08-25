import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

ACCESS_TOKEN_TTL_SECONDS = 900  # 15 minutes
REFRESH_TOKEN_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 days


def _encode(user_id: str, token_type: str, ttl_seconds: int) -> str:
    payload = {
        "user_id": user_id,
        "type": token_type,
        "exp": int(time.time()) + ttl_seconds,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_pair_response(user_id: str) -> Dict[str, str]:
    """Issue a fresh access/refresh token pair for the given user id."""
    return {
        "access_token": _encode(user_id, "access", ACCESS_TOKEN_TTL_SECONDS),
        "refresh_token": _encode(user_id, "refresh", REFRESH_TOKEN_TTL_SECONDS),
    }


def decode_jwt(token: str, expected_type: str = "access") -> dict | None:
    """Decode and verify a JWT of the given type, returning its payload or None if invalid/expired/wrong type."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None

    if payload.get("type") != expected_type:
        return None

    return payload


def refresh_access_token(token: str) -> Dict[str, str] | None:
    """Exchange a valid, non-expired refresh token for a new access/refresh token pair."""
    payload = decode_jwt(token, expected_type="refresh")
    if payload is None:
        return None

    return token_pair_response(payload["user_id"])