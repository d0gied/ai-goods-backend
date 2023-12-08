from ..base import BaseTask


class BaseParserTask(BaseTask):
    queue = "default"

    def __init__(self, name: str):
        super().__init__("parser", name)

    def run(self, *args, **kwargs):
        pass
