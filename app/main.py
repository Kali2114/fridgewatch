from fastapi import FastAPI
from app.api.items import router as items_router

app = FastAPI()
app.include_router(items_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}