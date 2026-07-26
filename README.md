# FastAPI Recipes 🍉

A small FastAPI service for saving and retrieving recipes, with JWT-based user auth.

## Stack

- **FastAPI** — HTTP API
- **SQLAlchemy 2.0 (async)** + **asyncpg** — ORM / Postgres driver
- **Alembic** — database migrations
- **PyJWT** — auth tokens
- **uv** — dependency management / running

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Docker (for the local Postgres instance)

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Copy the example environment file and adjust if needed:

   ```bash
   cp .env.example .env
   ```

   | Variable        | Description                                    |
   | --------------- | ----------------------------------------------- |
   | `DB_URL`        | Async SQLAlchemy URL, e.g. `postgresql+asyncpg://user:pass@host:5432/db` |
   | `JWT_SECRET`    | Secret used to sign auth tokens                  |
   | `JWT_ALGORITHM` | JWT signing algorithm, e.g. `HS256`              |

3. Start Postgres:

   ```bash
   docker compose up -d
   ```

4. Apply database migrations:

   ```bash
   uv run alembic upgrade head
   ```

## Running the app

```bash
uv run uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

## Database migrations

Migrations are managed with Alembic and live in `alembic/versions/`.

- Create a migration after changing a model in `app/models/`:

  ```bash
  uv run alembic revision --autogenerate -m "describe the change"
  ```

- Apply pending migrations:

  ```bash
  uv run alembic upgrade head
  ```

- Roll back the last migration:

  ```bash
  uv run alembic downgrade -1
  ```

## Project layout

```
app/
  api/        # FastAPI routers (recipes, user)
  auth/       # JWT signing/verification, auth dependency
  core/       # settings and DB session/engine
  models/     # SQLAlchemy ORM models
  schemas/    # Pydantic request/response schemas
alembic/      # migration environment and versions
```
