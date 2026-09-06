# fridgewatch — "What The Fridge?"

Fridge inventory portfolio app. You add what you currently have in your fridge; the app tracks
expiration dates and sends alerts ("eat this today or tomorrow you'll be doing archaeology"),
and later suggests sensible meals from what you have on hand.

Frontend: product photos, drag-and-drop, an expiration timeline.
Backend: FastAPI, authentication, inventory management, background reminders, optional OCR/AI.

## Stack
FastAPI, uvicorn, pytest, httpx (TestClient), APScheduler (in-process), SQLite.
No JS framework — `/docs` is the dev UI; a plain HTML+fetch page ships with the v1 dashboard.

## Workflow rules
- **TDD, domain-first.** Pure Python classes + tests before any web/FastAPI layer.
- Domain logic stays free of framework imports; clocks/time are always injected, never `datetime.now()` inline.
- When the user says **"check"**, they want a code review (hints/pointers, not a rewritten solution — they're
  practicing solo coding and want to write the fix themselves).
- Commit and push in small increments, only when the user explicitly asks.

## v1 scope (ship & deploy before anything else)
- Auth: register/login, hashed passwords
- Fridge inventory CRUD: item name, quantity, added date, expiry date
- Expiry dashboard: items sorted by days-until-expiry, traffic-light/timeline view
- One daily in-process APScheduler job emailing "these items expire within 2 days"

## Later milestones (not before v1 is deployed)
1. Recipe matching (dumb first: recipe needs {a,b,c}, have 2/3 → show the gap; no AI)
2. Item photos
3. OCR/LLM receipt scanning (last)

## Current status
- **Domain layer done** (TDD, no web deps):
  - `app/domain/inventory.py`: `Item(user_id, name, quantity, added_date, expiry_date, id=None)`.
    `quantity` is a validated `@property` (`<=0` raises `ValueError`); `__init__` assigns through it.
    `days_until_expiry(today)`, `status(today) -> ExpiryStatus` (FRESH / EXPIRING_SOON `<=2d` / EXPIRED `<0d`).
  - `app/domain/repository.py`: `InMemoryItemRepository` — `add_item` (sequential id from 1), `get_item`,
    `list_for_user`, `delete_item`, `update_item(id, payload_dict)` (blind `setattr`, no field whitelist —
    Pydantic guards this at the route). Missing id raises `ItemNotFound` (`app/domain/exceptions.py`,
    base `DomainError`). Repo is dumb storage — ownership checks belong in the web layer.
  - Tests use `tests/domain/utils.py::create_item(**kwargs)` factory.
- **Web layer started:**
  - `app/main.py`: FastAPI app + `GET /health`.
  - `app/api/items.py`: `POST /items` (201) using `ItemCreate`/`ItemRead` schemas in `app/schemas.py`
    (`ItemRead` uses `from_attributes`; `ItemCreate.quantity` is `Field(gt=0)` → 422 on bad input before the route).
  - `app/dependencies.py::get_repository` returns a module-level `InMemoryItemRepository`;
    `tests/api/conftest.py::fresh_repository` overrides it per test via `app.dependency_overrides`.
  - `user_id` is hardcoded to `1` in the route until auth exists.
  - 23 tests green.

## Next up
- Remaining CRUD routes: `GET /items` (list — dashboard needs it), `GET /items/{id}`, `PUT`, `DELETE`.
- `GET /items/{id}` needs `@app.exception_handler(DomainError)` mapping `ItemNotFound` → 404.
- Then SQLAlchemy persistence, then auth.
