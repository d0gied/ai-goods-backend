import warnings
from parser.models import Good
from parser.parsers.ozon import OZONParser

import pytest


def test_get_goods():
    return warnings.warn("Not implemented")
    parser = OZONParser()
    parser.get_goods("request", limit=10)
    goods = parser.get_goods("request", limit=10)
    assert isinstance(goods, list)
    assert all(isinstance(good, Good) for good in goods)
    assert len(goods) <= 10


def test_get_good():
    return warnings.warn("Not implemented")
    parser = OZONParser()
    good = parser.get_good("good_id")
    assert isinstance(good, Good)
    # Add more assertions to test the behavior of the get_good method
