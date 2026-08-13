import json

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from google.genai import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.models import RecipeModel
from app.schemas import CreateRecipeSchema, RecipeAIResponse, RecipeSchema
from app.utils.auth import get_current_user_id
from app.utils.gemini.gemini_client import client as gemini_client
recipes_router = APIRouter()

@recipes_router.get("/recipes")
async def get_recipe_by_owner_id(
    owner_id: int = Depends(get_current_user_id), session: AsyncSession = Depends(get_session)
) -> Page[RecipeSchema]:
    """List recipes owned by the authenticated user, paginated."""
    query = select(RecipeModel).where(RecipeModel.owner_id == owner_id).order_by(RecipeModel.id)
    return await sqlalchemy_paginate(session, query)
    # TODO: Write some tests


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
    # TODO: Write some tests




@recipes_router.post("/create-recipe-ai")
async def create_recipe_by_ingredients(
    ingredients: list[str],
    session: AsyncSession = Depends(get_session),
    owner_id: int = Depends(get_current_user_id),
):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""
        Create a complete recipe using these ingredients:

        {ingredients}

        The recipe should be practical and actually cookable.
        You may use basic additional ingredients such as salt, pepper, oil,
        water, or common spices when necessary.
        """,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RecipeAIResponse,
        ),
    )

    return json.loads(response.text)