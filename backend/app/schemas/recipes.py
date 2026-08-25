from datetime import datetime

from pydantic import BaseModel, ConfigDict

class CreateRecipeSchema(BaseModel):
    """Request body for creating a recipe."""

    title: str
    cuisine: str
    steps: list[str]
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


class RecipeAIResponse(BaseModel):
    title: str
    cuisine: str | None
    servings: int
    ingredients: list[str]
    steps: list[str]



# class RecipeGenerateRequest(BaseModel):
#     ingredients: list[str] = Field(
#         ..., min_length=1, examples=[["rice", "chicken", "tomatos"]]
#     )
#     extra_ingredients_include: bool = False
#     cuisine: str | None = Field(default=None, examples=["Italian"])
#     servings: int = Field(default=2, ge=1, le=10)
#     dietary_restrictions: list[str] = Field(
#         default_factory=list, examples=[["gluten-free"]]
#     )
#     extra_notes: str | None = Field(
#         default=None, max_length=500, examples=["Ready in under 30 minutes"]
#     )


# class GeneratedRecipe(BaseModel):
#     title: str = Field(..., max_length=250)
#     description: str = Field(..., max_length=500)
#     cuisine: str | None = Field(default=None, max_length=100)
#     servings: int
#     cook_time_minutes: int = Field(..., ge=0)
#     prep_time_minutes: int = Field(..., ge=0)
#     ingredients: list[str] = Field(..., min_length=1)
#     steps: list[str] = Field(..., min_length=1)