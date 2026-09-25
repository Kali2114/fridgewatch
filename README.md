# What The Fridge?

A fridge inventory tracker: log what's in your fridge, get alerted before it expires, and see
which recipes you're closest to being able to cook with what's on hand. Built as a from-scratch
FastAPI backend with a hand-built interactive frontend — no JS framework, no CRUD-generator
boilerplate.

## Features

- **Auth** — register/login with hashed passwords (bcrypt) and JWT-based sessions.
- **Fridge inventory** — full CRUD for items (name, quantity, added/expiry date), each scoped to
  its owner. Attach a photo to any item via a validated multipart upload.
- **Expiry dashboard** — items sorted soonest-to-expire first, tagged `fresh` / `expiring_soon` /
  `expired`.
- **Daily reminder email** — a background job (APScheduler, in-process) emails each user a summary
  of what's expiring within 2 days.
- **Recipe matching** — a seeded recipe catalog ranked against your current fridge contents, showing
  exactly which ingredients you're missing for each one (name matching is case/whitespace-insensitive,
  so "Eggs" in your fridge still satisfies a recipe that lists "eggs").
- **Interactive fridge UI** — a hand-drawn, animated fridge you click open to reveal your items
  (each shown with its photo and an expiry-colored ring) and a recipe-suggestions panel that slides
  out once the door opens.

## Stack

FastAPI · SQLAlchemy + Alembic migrations · SQLite · APScheduler · pytest (100% line coverage) ·
plain HTML/CSS/JS frontend (no framework).

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.sample .env   # fill in a JWT secret and SMTP credentials

alembic upgrade head   # create the database schema
uvicorn app.main:app --reload
```

The dashboard is served at `http://localhost:8000/`; interactive API docs at `/docs`.

## Testing

```bash
pytest
```

Pre-commit hooks (ruff, black) and GitHub Actions CI run lint + the full test suite on every push.

## Project layout

```
app/
  domain/          # pure Python business logic — no framework imports
  infrastructure/   # SQLAlchemy models & repositories
  api/              # FastAPI routers
  schemas.py        # Pydantic request/response models
alembic/            # database migrations
static/index.html    # the frontend
tests/                # mirrors app/ — domain, infrastructure, and api layers each tested in isolation
```

Domain logic is built and tested independently of the web/database layers (TDD, domain-first) —
e.g. `app/domain/recipe.py`'s ingredient-matching logic has no dependency on FastAPI or SQLAlchemy
at all.
