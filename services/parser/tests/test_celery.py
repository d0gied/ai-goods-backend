from parser.models import Good
from parser.parsers.base import Parser
from parser.tasks.get_good import GetGoodTask, get_good_task_builder
from parser.tasks.get_goods import (
    GetGoodsMultipleSourcesTask,
    GetGoodsTask,
)


class MockParser(Parser):
    source = "mock"

    def get_good(self, good_id: int, **kwargs) -> Good:
        return Good(id=good_id, name="Mock Good")

    def get_goods(self, request: str, *, limit: int = 100, **kwargs) -> list[Good]:
        return [Good(id=i, name=f"Mock Good {i}") for i in range(limit)]


def test_get_good_task_run():
    parser = MockParser()
    task = GetGoodTask(name="test_task", parser=parser)
    good = task.run(good_id=1)

    assert isinstance(good, dict)
    assert good["id"] == 1
    assert good["name"] == "Mock Good"


def test_get_good_task_builder():
    parser = MockParser()
    task = GetGoodTask(name="test_task", parser=parser)
    task_builder = get_good_task_builder(name="test_task", parser=parser)
    assert isinstance(task_builder, GetGoodTask)
    assert task_builder.name == task.name
    assert task_builder.parser == task.parser


def test_get_goods_from_source_task_run():
    parser = MockParser()
    task = GetGoodsTask(name="test_task", parser=parser)
    goods = task.run(request="test_request", limit=10)

    assert isinstance(goods, list)
    assert len(goods) == 10
    for i, good in enumerate(goods):
        assert isinstance(good, dict)
        assert good["id"] == i
        assert good["name"] == f"Mock Good {i}"


def test_get_goods_from_source_task_builder():
    parser = MockParser()
    task = GetGoodsTask(name="test_task", parser=parser)
    task_builder = GetGoodsTask(name="test_task", parser=parser)
    assert isinstance(task_builder, GetGoodsTask)
    assert task_builder.name == task.name
