from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.items import router as items_router
from app.api.recipes import router as recipes_router
from app.domain.exceptions import EmailAlreadyRegistered, ItemNotFound, RecipeNotFound
from app.infrastructure.database import Base, engine
from app.jobs import run_scheduled_reminder_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_scheduled_reminder_job, "cron", hour=8)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(auth_router)
app.include_router(recipes_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse("static/index.html")


@app.exception_handler(ItemNotFound)
def item_not_found_handler(request: Request, exc: ItemNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(EmailAlreadyRegistered)
def email_already_registered_handler(request: Request, exc: EmailAlreadyRegistered):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(RecipeNotFound)
def recipe_not_found_handler(request: Request, exc: RecipeNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}
