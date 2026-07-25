from pydantic import BaseModel

class CreateRecipeSchema(BaseModel):
    title: str
    cuisine: str
    steps: int
    servings: int
    ingredients: list[str]
    