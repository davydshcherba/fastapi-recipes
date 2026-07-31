from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.utils.auth import get_current_user_id
from app.core.db import get_session
from app.models import CategoryModel, RecipeModel
from app.schemas import CreateCategorySchema, UpdateCategorySchema

categories_router = APIRouter()


async def _get_owned_category(id: int, owner_id: int, session: AsyncSession) -> CategoryModel:
    """Fetch a category by id and ensure the authenticated user owns it."""
    result = await session.execute(
        select(CategoryModel).options(selectinload(CategoryModel.recipes)).where(CategoryModel.id == id)
    )
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if category.owner_id != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your category")

    return category


@categories_router.get("/categories")
async def get_categories(session: AsyncSession = Depends(get_session), owner_id: int = Depends(get_current_user_id)):
    """List all categories, regardless of owner."""
    result = await session.execute(
        select(CategoryModel).options(selectinload(CategoryModel.recipes)).where(CategoryModel.owner_id == owner_id)
    )
    return result.scalars().all()


@categories_router.get("/categories/{id}")
async def get_category(id: int, session: AsyncSession = Depends(get_session)):
    """Fetch a single category by id, together with its recipes."""
    result = await session.execute(
        select(CategoryModel).options(selectinload(CategoryModel.recipes)).where(CategoryModel.id == id)
    )
    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return category


@categories_router.post("/categories")
async def create_category(
    data: CreateCategorySchema,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Create a category owned by the authenticated user."""
    category = CategoryModel(name=data.name, owner_id=owner_id)
    session.add(category)
    await session.commit()
    await session.refresh(category)

    return category


@categories_router.put("/categories/{id}")
async def update_category(
    id: int,
    data: UpdateCategorySchema,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Rename a category owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)

    category.name = data.name
    await session.commit()
    await session.refresh(category)

    return category


@categories_router.delete("/categories/{id}")
async def delete_category(
    id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Delete a category owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)

    await session.delete(category)
    await session.commit()

    return {"detail": "Category deleted"}


@categories_router.post("/categories/{id}/recipes/{recipe_id}")
async def add_recipe_to_category(
    id: int,
    recipe_id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Attach a recipe to a category owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)
    recipe = await session.get(RecipeModel, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if recipe not in category.recipes:
        category.recipes.append(recipe)
        await session.commit()
        await session.refresh(category)

    return category


@categories_router.delete("/categories/{id}/recipes/{recipe_id}")
async def remove_recipe_from_category(
    id: int,
    recipe_id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Detach a recipe from a category owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)
    recipe = await session.get(RecipeModel, recipe_id)

    if recipe is not None and recipe in category.recipes:
        category.recipes.remove(recipe)
        await session.commit()
        await session.refresh(category)

    return category
