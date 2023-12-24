from fastapi import APIRouter

from .embed import router as embed_router
from .parse import router as parse_router
from .search import router as search_router

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(embed_router)
router.include_router(parse_router)
router.include_router(search_router)


def get_routers():
    return router
