import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + 900
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None