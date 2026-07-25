from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models import RecipeModel

recipes_router = APIRouter()

@recipes_router.get("/recipes")
async def get_recipes(id: int, session: AsyncSession = Depends(get_session)):
    recipe = await session.execute(select(RecipeModel).where(RecipeModel.id == id))

    result = recipe.scalar_one_or_none()

    return result

