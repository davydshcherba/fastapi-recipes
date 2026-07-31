from datetime import datetime

from pydantic import BaseModel, ConfigDict

class CreateRecipeSchema(BaseModel):
    """Request body for creating a recipe."""

    title: str
    cuisine: str
    steps: int
    servings: int
    ingredients: list[str]


class RecipeSummary(BaseModel):
    """Minimal recipe representation, used when nested under a category."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class RecipeSchema(BaseModel):
    """Response body for a recipe."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    cuisine: str | None
    servings: int
    ingredients: list[str]
    steps: list[str]
    owner_id: int
    created_at: datetime
