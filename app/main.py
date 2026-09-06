from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.items import router as items_router
from app.domain.exceptions import ItemNotFound

app = FastAPI()
app.include_router(items_router)


@app.exception_handler(ItemNotFound)
def item_not_found_handler(request: Request, exc: ItemNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}
