from fastapi import APIRouter, Depends, HTTPException
from global_modules.models import Good

from ..tasks.search import SearchTask
from ..utils import JSONResponse

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

    task = SearchTask()

    if not name and not image:
        raise HTTPException(
            status_code=400, detail="Bad request, name or image required"
        )
    if not image:
        good = Good(name=name)
    else:
        good = Good(name=name, images=[image])

    task_status = task.run(good, limit=limit)

    response = {
        "status": "ok",
        "task_id": task_status.id,
    }

    return JSONResponse(response)


@router.get("/{task_id}")
def get_search(task_id: str):
    """Get search status

    Args:
        task_id (str): Task ID

    Returns:
        JSONResponse: Task status
    """

    task = SearchTask()
    task = task.get_status(task_id, ignore_name=True)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    response = {
        "status": task.state,
    }
    if task.state == "SUCCESS":
        response["result"] = task.result

    return JSONResponse(response)
