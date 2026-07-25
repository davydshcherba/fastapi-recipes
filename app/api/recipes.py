from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models import RecipeModel
from app.schemas import CreateRecipeSchema

recipes_router = APIRouter()

@recipes_router.get("/recipes")
async def get_recipe(id: int, session: AsyncSession = Depends(get_session)):
    recipe = await session.execute(select(RecipeModel).where(RecipeModel.id == id))

    result = recipe.scalar_one_or_none()

    return result


@recipes_router.post("/recipes")
async def create_recipe(data: CreateRecipeSchema,session: AsyncSession = Depends(get_session)):
    recipe = RecipeModel(title=data.title, cuisine=data.cuisine, servings=data.servings, steps=data.steps,ingredients=data.ingredients, owner_id=2)
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)

    return recipe
