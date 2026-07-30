from pydantic import BaseModel

class CreateCategorySchema(BaseModel):
    """Request body for creating a category."""

    name: str

class UpdateCategorySchema(BaseModel):
    """Request body for renaming a category."""

    name: str
