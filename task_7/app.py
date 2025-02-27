from fastapi import APIRouter, FastAPI
from routes import router
app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(router, prefix="")

app.include_router(v1_router)