from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import signJWT
from app.core.db import get_session
from app.models import UserModel

user_router = APIRouter()


@user_router.post("/login")
async def login_user(username: str, password: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalar_one_or_none()

    if user is None or user.hashed_password != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return signJWT(user.id)

@user_router.post("/register")
async def register_user(username: str, password: str, session: AsyncSession = Depends(get_session)):
    user = UserModel(username=username, hashed_password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return signJWT(user.id)