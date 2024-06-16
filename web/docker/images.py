from fastapi import APIRouter as Router, HTTPException
from dto.controllers.image import CreateImage, PullImage, RemoveImage
from docker_management.docker_client import client

router = Router()


@router.get("/image")
async def list_images():
    status, success, content = client.images.images_list(json=True)

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.get("/image/{image_name}")
async def get_image(image_name: str):
    status, success, content = client.images.get_image(image_name=image_name, json=True)

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.post("/image")
async def create_image(image_data: CreateImage):
    if image_data:
        status, success, content = client.images.build_image(
            title=image_data.title,
            tag=image_data.tag,
            layers=image_data.layers,
            files=image_data.files,
        )
    else:
        raise HTTPException(status_code=400, detail="Image creation data is required")

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": {"image": content[0], "logs": content[1]}}


@router.post("/image/pull")
async def pull_image(data: PullImage):
    status, success, content = client.images.pull_image(
        repository=data.repository, tag=data.tag, json=True
    )

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.delete("/image")
async def remove_image(data: RemoveImage):

    status, success, content = client.images.remove_image(
        data.image, data.force, data.pruned
    )

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"message": content}
