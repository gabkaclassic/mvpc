from fastapi import APIRouter as Router, HTTPException
from starlette.websockets import WebSocket
from dto.controllers.container import CreateContainer, StopContainer, RemoveContainer
from docker_management.docker_client import client

router = Router()


@router.get("/container")
async def list_containers():
    status, success, content = client.containers.containers_list(json=True)

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.get("/container/{container_id}")
async def get_container(container_id: str):
    status, success, content = client.containers.get_container(
        container_id=container_id, json=True
    )

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"data": content}


@router.get("/container/{container_id}/logs")
async def get_container_logs(container_id: str):
    status, success, content = client.containers.get_container_logs(container_id)

    if not success:
        raise HTTPException(status_code=status, detail=content)

    return {"logs": content}


@router.websocket("/container/{container_id}/logs/stream")
async def get_container_logs_stream(container_id: str, websocket: WebSocket):
    try:
        await websocket.accept()

        logs_generator = client.containers.get_container_logs_stream(
            container_id=container_id
        )
        for log_line in logs_generator:
            await websocket.send_text(log_line)
    except Exception as e:
        await websocket.send_text("Internal Server Error")
    finally:
        await websocket.close()


@router.websocket("/container/{container_id}/command")
async def execute_container_command(container_id: str, websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            command = await websocket.receive_text()
            result_generator = client.containers.execute_command(container_id, command)
            for result_line in result_generator:
                await websocket.send_text(result_line)
    except Exception as e:
        await websocket.send_text("Internal Server Error")
    finally:
        await websocket.close()


@router.post("/container")
async def create_container(data: CreateContainer):
    value, success, details = client.containers.create_container(
        data.name, data.image, json=True
    )

    if not success:
        raise HTTPException(status_code=value, detail=details)

    return {"data": value, "detail": details}


@router.delete("/container")
async def delete_container(data: RemoveContainer):
    result, success, details = client.containers.remove_container(data.id, data.force)

    if not success:
        raise HTTPException(status_code=result, detail=details)

    return {"data": result, "detail": details} @ router.delete("/container")


@router.post("/container/stop")
async def stop_container(data: StopContainer):
    result, success, details = client.containers.stop_container(data.id)

    if not success:
        raise HTTPException(status_code=result, detail=details)

    return {"data": result, "detail": details}
