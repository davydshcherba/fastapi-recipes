from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.auth import Hasher, refresh_access_token, token_pair_response
from app.core.db import get_session
from app.models import UserModel
from app.schemas import LoginSchema, RefreshTokenSchema, RegisterSchema

user_router = APIRouter()


@user_router.post("/login")
async def login_user(data: LoginSchema, session: AsyncSession = Depends(get_session)):
    """Authenticate a user by username/password and return an access/refresh token pair."""
    result = await session.execute(select(UserModel).where(UserModel.username == data.username))
    user = result.scalar_one_or_none()

    if user is None or not Hasher.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return token_pair_response(user.id)

@user_router.post("/register")
async def register_user(data: RegisterSchema, session: AsyncSession = Depends(get_session)):
    """Create a new user account and return an access/refresh token pair for it."""
    user = UserModel(username=data.username, hashed_password=Hasher.get_password_hash(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return token_pair_response(user.id)

@user_router.post("/refresh")
async def refresh_token(data: RefreshTokenSchema):
    """Exchange a valid refresh token for a new access/refresh token pair."""
    tokens = refresh_access_token(data.refresh_token)
    if tokens is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    return tokens