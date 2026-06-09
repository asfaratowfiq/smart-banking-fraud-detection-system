from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.status import (
    router as status_router
)
from app.api.result import (
    router as result_router
)
app = FastAPI(
    title="Smart Banking Fraud Detection System",
    version="1.0.0"
)
app.include_router(
    upload_router,
    prefix="/api/v1"
)
app.include_router(
    status_router,
    prefix="/api/v1"
)
app.include_router(
    result_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {"message": "API Running"}

@app.get("/health")
def health():
    return {"status": "UP"}