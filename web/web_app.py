from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .docker.containers import router as container_router
from .docker.images import router as image_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(container_router)
app.include_router(image_router)
