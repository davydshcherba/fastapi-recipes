from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.utils.auth import get_current_user_id
from app.core.db import get_session
from app.models import CategoryModel, RecipeModel
from app.schemas import CategorySchema, CreateCategorySchema, UpdateCategorySchema

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
async def get_categories(
    session: AsyncSession = Depends(get_session), owner_id: int = Depends(get_current_user_id)
) -> Page[CategorySchema]:
    """List all categories owned by the authenticated user, paginated."""
    query = (
        select(CategoryModel)
        .options(selectinload(CategoryModel.recipes))
        .where(CategoryModel.owner_id == owner_id)
        .order_by(CategoryModel.id)
    )
    return await sqlalchemy_paginate(session, query)
    # TODO: Write some tests


@categories_router.get("/categories/{id}")
async def get_category(
    id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Fetch a single category owned by the authenticated user, together with its recipes."""
    return await _get_owned_category(id, owner_id, session)
    # TODO: Write some tests


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
    # TODO: Write some tests

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
    # TODO: Write some tests


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
    # TODO: Write some tests


async def _get_owned_recipe(id: int, owner_id: int, session: AsyncSession) -> RecipeModel:
    """Fetch a recipe by id and ensure the authenticated user owns it."""
    recipe = await session.get(RecipeModel, id)

    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    if recipe.owner_id != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your recipe")

    return recipe
    # TODO: Write some tests


@categories_router.post("/categories/{id}/recipes/{recipe_id}")
async def add_recipe_to_category(
    id: int,
    recipe_id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Attach a recipe to a category, both owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)
    recipe = await _get_owned_recipe(recipe_id, owner_id, session)

    if recipe not in category.recipes:
        category.recipes.append(recipe)
        await session.commit()
        await session.refresh(category)

    return category
    # TODO: Write some tests


@categories_router.delete("/categories/{id}/recipes/{recipe_id}")
async def remove_recipe_from_category(
    id: int,
    recipe_id: int,
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    """Detach a recipe from a category, both owned by the authenticated user."""
    category = await _get_owned_category(id, owner_id, session)
    recipe = await _get_owned_recipe(recipe_id, owner_id, session)

    if recipe in category.recipes:
        category.recipes.remove(recipe)
        await session.commit()
        await session.refresh(category)

    return category
    # TODO: Write some tests