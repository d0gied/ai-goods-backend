from ..parsers.base import Parser
from .base import BaseTask


class GetGoodTask(BaseTask):
    """Parser task with prerealized logic for parsing to be used in subclasses

    Args:
        name (str): name of the task
        parser (Parser): parser instance
    """

    def __init__(self, name: str, parser: Parser):
        super().__init__(f"get_good.{name}")
        self.parser = parser

    def run(self, good_id: str, **kwargs) -> dict:
        """Run the task"""

        # TODO: add logging
        # TODO: add error handling
        # TODO: add retrying
        # TODO: add saving storage(db, file system, S3, etc.)
        # TODO: change returning value to returning file name

        return self.parser.get_good(good_id=good_id, **kwargs).model_dump()


def get_good_task_builder(name: str, parser: Parser) -> GetGoodTask:
    """Get GetGoodTask instance"""
    return GetGoodTask(name=name, parser=parser)
