import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..tasks.parse import ParseWildberriesTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/parse",
    tags=["parse"],
    responses={404: {"description": "Not found"}},
)


@router.post("/wildberries")
def start_parse_wildberries(request: str, limit: int = 100):
    """Start parse wildberries"""
    task = ParseWildberriesTask()
    task_status = task.run(request, limit=limit)

    return JSONResponse(
        {
            "status": "ok",
            "task_id": task_status.id,
        }
    )


@router.get("/wildberries/{task_id}")
def get_parse_wildberries(task_id: str):
    """Get parse wildberries status"""
    task = ParseWildberriesTask()
    task = task.get_status(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    response = {
        "task_id": task.id,
        "status": task.state,
    }
    if task.state == "SUCCESS":
        response["result"] = task.result
    else:
        response["error"] = task.traceback

    return JSONResponse(response)
