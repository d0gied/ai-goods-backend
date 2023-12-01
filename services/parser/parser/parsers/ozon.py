from parser.models import Good
from .base import Parser


class OZONParser(Parser):
    """Ozon parser"""

    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        # TODO: Implement this method
        raise NotImplementedError

    def get_good(self, good_id: str, **kwargs) -> Good:
        # TODO: Implement this method
        raise NotImplementedError
