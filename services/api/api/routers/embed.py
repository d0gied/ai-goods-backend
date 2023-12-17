import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException

from ..tasks.embed import ReembedAllGoodsTask
from ..utils import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/embed",
    tags=["embed"],
    responses={404: {"description": "Not found"}},
)


@router.post("/reembed/{target}")
def start_parse_wildberries(target: Literal["name", "image", "name_image", "all"]):
    """Start parse wildberries"""
    task = ReembedAllGoodsTask()
    task_status = task.run(target=target)

    return JSONResponse(
        {
            "status": "ok",
            "task_id": task_status.id,
        }
    )
