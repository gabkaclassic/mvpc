from fastapi import FastAPI
from .docker.containers import router as container_router

app = FastAPI()
app.include_router(container_router)
