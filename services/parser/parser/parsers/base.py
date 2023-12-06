from abc import ABC

from ..models import Good


class Parser(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        """Get goods from the site

        P.s. Without images

        Args:
            request (str): request for search
            limit (int, optional): Max amount of goods to search. Defaults to 100.
        Returns:
            list[Good]: list of goods
        """

        raise NotImplementedError

    def get_good(self, good_id: int, **kwargs) -> Good:
        """Get good from the site

        Args:
            good_id (str): good id

        Returns:
            Good: good
        """

        raise NotImplementedError
