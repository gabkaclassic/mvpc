from io import BytesIO

from fastapi import APIRouter as Router, HTTPException, UploadFile, File, Form
from pydantic import BaseModel as Model
from typing import Annotated

from docker_management.docker_client import client

router = Router()


@router.get("/image")
async def list_images():
    status, success, content = client.images.images_list(json=True)

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.post("/image")
async def create_image(
    dockerfile: Annotated[UploadFile, File()] = None,
    path: Annotated[str, Form()] = None,
    tag: Annotated[str, Form()] = None,
):
    if path:
        status, success, content = client.images.build_image(
            path=path, tag=tag, json=True
        )
    elif dockerfile:
        file_content = await dockerfile.read()
        with BytesIO(file_content) as file_stream:
            status, success, content = client.images.build_image(
                dockerfile=file_stream, tag=tag, json=True
            )
    else:
        raise HTTPException(status_code=400, detail="Dockerfile or path required")

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": {"image": content[0], "logs": content[1]}}


class PullImage(Model):
    repository: str
    tag: str


@router.post("/image/pull")
async def pull_image(data: PullImage):
    status, success, content = client.images.pull_image(
        repository=data.repository, tag=data.tag, json=True
    )

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


class RemoveImage(Model):
    image: str
    force: bool = False
    pruned: bool = False


@router.delete("/image")
async def remove_image(data: RemoveImage):

    status, success, content = client.images.remove_image(
        data.image, data.force, data.pruned
    )

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"message": content}
