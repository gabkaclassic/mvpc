from fastapi import FastAPI
from .docker.containers import router as container_router
from .docker.images import router as image_router

app = FastAPI()

app.include_router(container_router)
app.include_router(image_router)
