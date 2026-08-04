from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api import user_router
from app.api import recipes_router
from app.api import categories_router
from google import genai
from app.core.config import settings

app = FastAPI(
        title="FastAPI recipe 🍉",
    )
add_pagination(app)

client = genai.Client(api_key=settings.gemini_api_key)

@app.get("/health", tags=["Health 🏥"])
def health():
    """ HEALTH CHECKER """
    return "OK OK OK"

app.include_router(user_router,tags=["User 🙆‍♂️"])
app.include_router(recipes_router, tags=["Recipes 🍰"])
app.include_router(categories_router, tags=["Categories 🏷️"])

@app.get("/hello", tags=["Hello 🌍"])
def hello():
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Explain how AI works in a few words",
    )

    return {"text": response.text}