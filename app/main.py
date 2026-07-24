from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import init_db
from app.models import RecipeModel, UserModel  # noqa: F401  ensure models are registered on metadata
from app.api import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    """ HEALTH CHECKER """
    return "OK OK OK"

app.include_router(user_router,tags=["USER"])
