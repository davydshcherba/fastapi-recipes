from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .recipes import RecipeModel
    from .user import UserModel


recipe_category_table = Table(
    "recipe_category",
    Base.metadata,
    Column[Any]("recipe_id", ForeignKey("recipe.id"), primary_key=True),
    Column[Any]("category_id", ForeignKey("category.id"), primary_key=True),
)


class CategoryModel(Base):
    """A user-defined grouping for recipes."""

    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    owner: Mapped["UserModel"] = relationship(back_populates="categories")
    recipes: Mapped[list["RecipeModel"]] = relationship(
        secondary=recipe_category_table, back_populates="categories"
    )
