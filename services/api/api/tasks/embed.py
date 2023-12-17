from typing import Literal

from .base import BaseTask


class ReembedAllGoodsTask(BaseTask):
    name = "agent.tasks.reembed_all_goods"
    queue = "agent"

    def run(
        self, target: Literal["name", "image", "name_image", "all"] = "all", **kwargs
    ) -> None:
        return super().run(target=target, **kwargs)
