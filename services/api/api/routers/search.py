from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..tasks.parse import ParseWildberriesTask

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search")
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
