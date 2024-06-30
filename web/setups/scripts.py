from fastapi import APIRouter as Router
from fastapi import HTTPException

router = Router()


@router.get("/setup/{setup_id}")
async def get_setup_view(setup_id: str):
    pass


@router.get("/setup")
async def get_setup_list():
    pass


@router.post("/setup")
async def create_setup():
    pass


@router.delete("/setup/{setup_id}")
async def delete_setup():
    pass
