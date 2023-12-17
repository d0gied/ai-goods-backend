from celery.result import AsyncResult

from .base import BaseTask


class BaseParseTask(BaseTask):
    queue = "agent"

    def run(
        self, request: str, *, limit: int = 100, do_embed: bool = True, **kwargs
    ) -> AsyncResult:
        return super().run(request, limit=limit, do_embed=do_embed, **kwargs)


class ParseWildberriesTask(BaseParseTask):
    name = "agent.tasks.parse.wildberries"


class ParseAlibabaTask(BaseParseTask):
    name = "agent.tasks.parse.alibaba"


class ParseOZONTask(BaseParseTask):
    name = "agent.tasks.parse.ozon"
