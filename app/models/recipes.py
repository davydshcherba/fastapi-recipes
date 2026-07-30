from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .categories import recipe_category_table

if TYPE_CHECKING:
    from .categories import CategoryModel
    from .user import UserModel


class RecipeModel(Base):
    """A recipe a user chose to save."""

    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    cuisine: Mapped[str | None] = mapped_column(String(100), default=None)
    servings: Mapped[int] = mapped_column(default=2)
    ingredients: Mapped[list[str]] = mapped_column(JSON, default=list)  # free-text lines, no structured qty/unit
    steps: Mapped[list[str]] = mapped_column(JSON, default=list)  # ordered preparation steps

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    owner: Mapped["UserModel"] = relationship(back_populates="recipes")
    categories: Mapped[list["CategoryModel"]] = relationship(
        secondary=recipe_category_table, back_populates="recipes"
    )
