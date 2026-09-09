from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.auth import router as auth_router
from app.api.items import router as items_router
from app.domain.exceptions import EmailAlreadyRegistered, ItemNotFound
from app.infrastructure.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(auth_router)


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


@app.get("/health")
def health_check():
    return {"status": "ok"}
