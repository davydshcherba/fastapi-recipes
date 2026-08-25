from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.recipes import RecipeSummary

class CreateCategorySchema(BaseModel):
    """Request body for creating a category."""

    name: str

class UpdateCategorySchema(BaseModel):
    """Request body for renaming a category."""

    name: str


class CategorySchema(BaseModel):
    """Response body for a category."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner_id: int
    created_at: datetime
    recipes: list[RecipeSummary]
