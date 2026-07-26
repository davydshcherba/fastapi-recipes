from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user_id
from app.core.db import get_session
from app.models import RecipeModel
from app.schemas import CreateRecipeSchema

recipes_router = APIRouter()

@recipes_router.get("/recipes")
async def get_recipe(id: int, session: AsyncSession = Depends(get_session)):
    """Fetch a single recipe by id, regardless of owner."""
    recipe = await session.execute(select(RecipeModel).where(RecipeModel.id == id))

    result = recipe.scalar_one_or_none()

    return result


@recipes_router.post("/recipes")
async def create_recipe(
    data: CreateRecipeSchema,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Create a recipe owned by the authenticated user."""
    recipe = RecipeModel(title=data.title, cuisine=data.cuisine, servings=data.servings, steps=data.steps, ingredients=data.ingredients, owner_id=owner_id)
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)

    return recipe
