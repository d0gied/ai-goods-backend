from .base import BaseParserTask


class GetGoodTask(BaseParserTask):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(f"get_good.{name}")

    def run(self, request: str, *, limit=100, **kwargs) -> list[dict]:
        """Run the task"""
