from fastapi import FastAPI

from app.api import user_router
from app.api import recipes_router

app = FastAPI(
        title="FastAPI recipe 🍉",
    )


@app.get("/health", tags=["Health 🏥"])
def health():
    """ HEALTH CHECKER """
    return "OK OK OK"

app.include_router(user_router,tags=["User 🙆‍♂️"])
app.include_router(recipes_router, tags=["Recipes 🍰"])
