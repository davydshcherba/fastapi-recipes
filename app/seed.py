import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db import async_session_maker
from app.models import CategoryModel, RecipeModel, UserModel
from app.utils.auth import Hasher

TEST_USERNAME = "string"
TEST_PASSWORD = "string"

CATEGORY_NAMES = ["Сніданки", "Обіди", "Вечері", "Десерти", "Напої"]

RECIPES = [
    {
        "title": "Вівсянка з бананом",
        "cuisine": "Українська",
        "servings": 2,
        "ingredients": ["вівсяні пластівці", "молоко", "банан", "мед"],
        "steps": ["Закип'ятити молоко", "Всипати пластівці, варити 5 хв", "Додати нарізаний банан і мед"],
        "categories": ["Сніданки"],
    },
    {
        "title": "Омлет з сиром",
        "cuisine": "Французька",
        "servings": 1,
        "ingredients": ["яйця", "молоко", "твердий сир", "сіль"],
        "steps": ["Збити яйця з молоком і сіллю", "Смажити на сковороді 2 хв", "Посипати сиром і згорнути"],
        "categories": ["Сніданки"],
    },
    {
        "title": "Борщ",
        "cuisine": "Українська",
        "servings": 6,
        "ingredients": ["буряк", "капуста", "картопля", "морква", "цибуля", "яловичина"],
        "steps": ["Зварити бульйон з м'ясом", "Додати овочі по черзі", "Варити 40 хв, приправити"],
        "categories": ["Обіди", "Вечері"],
    },
    {
        "title": "Куряче філе з рисом",
        "cuisine": "Азійська",
        "servings": 3,
        "ingredients": ["куряче філе", "рис", "соєвий соус", "часник"],
        "steps": ["Обсмажити філе з часником", "Відварити рис", "Полити соєвим соусом і подавати разом"],
        "categories": ["Обіди"],
    },
    {
        "title": "Грецький салат",
        "cuisine": "Грецька",
        "servings": 4,
        "ingredients": ["огірки", "помідори", "фета", "оливки", "оливкова олія"],
        "steps": ["Нарізати овочі кубиками", "Додати фету й оливки", "Заправити оливковою олією"],
        "categories": ["Обіди", "Вечері"],
    },
    {
        "title": "Спагеті карбонара",
        "cuisine": "Італійська",
        "servings": 2,
        "ingredients": ["спагеті", "бекон", "яйця", "пармезан", "чорний перець"],
        "steps": ["Відварити спагеті", "Обсмажити бекон", "Змішати з яйцями та пармезаном поза вогнем"],
        "categories": ["Вечері"],
    },
    {
        "title": "Плов",
        "cuisine": "Узбецька",
        "servings": 6,
        "ingredients": ["рис", "баранина", "морква", "цибуля", "часник", "зіра"],
        "steps": ["Обсмажити м'ясо з цибулею й морквою", "Додати рис і воду", "Тушкувати під кришкою 30 хв"],
        "categories": ["Вечері"],
    },
    {
        "title": "Тірамісу",
        "cuisine": "Італійська",
        "servings": 8,
        "ingredients": ["маскарпоне", "яйця", "цукор", "савоярді", "кава", "какао"],
        "steps": ["Змішати маскарпоне з жовтками й цукром", "Вимочити печиво в каві", "Викласти шарами і охолодити"],
        "categories": ["Десерти"],
    },
    {
        "title": "Шарлотка з яблуками",
        "cuisine": "Українська",
        "servings": 6,
        "ingredients": ["яблука", "борошно", "цукор", "яйця"],
        "steps": ["Збити яйця з цукром", "Додати борошно й нарізані яблука", "Випікати 40 хв при 180°C"],
        "categories": ["Десерти"],
    },
    {
        "title": "Смузі з ягодами",
        "cuisine": "Американська",
        "servings": 2,
        "ingredients": ["полуниця", "банан", "йогурт", "мед"],
        "steps": ["Скласти всі інгредієнти в блендер", "Збити до однорідності", "Розлити по склянках"],
        "categories": ["Напої"],
    },
]


async def seed_test_user() -> UserModel:
    """Insert a test user (username/password 'string') if one doesn't already exist."""
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.username == TEST_USERNAME))
        user = result.scalar_one_or_none()
        if user is not None:
            print(f"User '{TEST_USERNAME}' already exists, skipping.")
            return user

        user = UserModel(username=TEST_USERNAME, hashed_password=Hasher.get_password_hash(TEST_PASSWORD))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"Created test user '{TEST_USERNAME}'.")
        return user


async def seed_categories(user: UserModel) -> dict[str, CategoryModel]:
    """Ensure the test user has the 5 seed categories, creating any that are missing."""
    async with async_session_maker() as session:
        result = await session.execute(select(CategoryModel).where(CategoryModel.owner_id == user.id))
        existing = {c.name: c for c in result.scalars().all()}

        for name in CATEGORY_NAMES:
            if name not in existing:
                category = CategoryModel(name=name, owner_id=user.id)
                session.add(category)
                existing[name] = category

        await session.commit()
        for category in existing.values():
            await session.refresh(category)

        print(f"Categories for '{TEST_USERNAME}': {len(existing)}.")
        return existing


async def seed_recipes(user: UserModel, categories: dict[str, CategoryModel]) -> None:
    """Ensure the test user has the 10 seed recipes, creating any that are missing."""
    async with async_session_maker() as session:
        result = await session.execute(select(RecipeModel).where(RecipeModel.owner_id == user.id))
        existing_titles = {r.title for r in result.scalars().all()}

        # re-fetch categories bound to this session, with recipes eager-loaded for the m2m assignment
        result = await session.execute(
            select(CategoryModel)
            .where(CategoryModel.owner_id == user.id)
            .options(selectinload(CategoryModel.recipes))
        )
        session_categories = {c.name: c for c in result.scalars().all()}

        created = 0
        for data in RECIPES:
            if data["title"] in existing_titles:
                continue

            recipe = RecipeModel(
                title=data["title"],
                cuisine=data["cuisine"],
                servings=data["servings"],
                ingredients=data["ingredients"],
                steps=data["steps"],
                owner_id=user.id,
                categories=[session_categories[name] for name in data["categories"]],
            )
            session.add(recipe)
            created += 1

        await session.commit()
        print(f"Created {created} new recipe(s) for '{TEST_USERNAME}'.")


async def main() -> None:
    user = await seed_test_user()
    categories = await seed_categories(user)
    await seed_recipes(user, categories)


if __name__ == "__main__":
    asyncio.run(main())
