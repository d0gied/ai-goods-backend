from .embed import router as embed_router
from .parse import router as parse_router
from .search import router as search_router


def get_routers():
    return [
        embed_router,
        parse_router,
        search_router,
    ]
