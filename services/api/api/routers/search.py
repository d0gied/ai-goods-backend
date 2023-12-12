from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..tasks.search import SearchByImageTask, SearchByNameImageTask, SearchByNameTask

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def start_search(name: str = None, image: str = None, limit: int = 100):
    """Start search by image

    Args:
        name (str): Good name
        image (str): Image URL
        limit (int, optional): Limit of results. Defaults to 100.

    Returns:
        JSONResponse: Task status
    """

    task = SearchByNameImageTask()
    task_status = task.run(name, image, limit=limit)


@router.get("/search/{task_id}")
def get_search_reuslt(task_id: str):
    """Get parse wildberries status"""
    task = ParseWildberriesTask()
    task = task.get_status(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return JSONResponse(
        {
            "task_id": task.id,
            "status": task.state,
            "result": task.result,
        }
    )
