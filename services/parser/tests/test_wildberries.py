from parser.models import Good
from parser.parsers.wildberries import WildberriesParser
import warnings


def test_get_goods():
    return warnings.warn("Not implemented")
    parser = WildberriesParser()
    goods = parser.get_goods("request", limit=10)
    assert isinstance(goods, list)
    assert all(isinstance(good, Good) for good in goods)
    assert len(goods) <= 10


def test_get_good():
    return warnings.warn("Not implemented")
    parser = WildberriesParser()
    good = parser.get_good("good_id")
    assert isinstance(good, Good)
    # Add more assertions to test the behavior of the get_good method
