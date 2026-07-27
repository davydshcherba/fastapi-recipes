from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.auth import Hasher, signJWT
from app.core.db import get_session
from app.models import UserModel

user_router = APIRouter()


@user_router.post("/login")
async def login_user(username: str, password: str, session: AsyncSession = Depends(get_session)):
    """Authenticate a user by username/password and return a signed JWT."""
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalar_one_or_none()

    if user is None or not Hasher.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return signJWT(user.id)

@user_router.post("/register")
async def register_user(username: str, password: str, session: AsyncSession = Depends(get_session)):
    """Create a new user account and return a signed JWT for it."""
    user = UserModel(username=username, hashed_password=Hasher.get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return signJWT(user.id)