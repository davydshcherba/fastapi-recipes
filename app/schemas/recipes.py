from pydantic import BaseModel

class CreateRecipeSchema(BaseModel):
    """Request body for creating a recipe."""

    title: str
    cuisine: str
    steps: int
    servings: int
    ingredients: list[str]
    