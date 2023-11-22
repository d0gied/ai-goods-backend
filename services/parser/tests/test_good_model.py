from datetime import datetime
from parser.models.good import Good

import pytest


def test_good():
    good = Good(
        id="test_good_id",
        name="test_good_name",
        description="test_good_description",
        price=100,
        currency="RUB",
        images=["test_good_image_1", "test_good_image_2"],
        url="test_good_url",
        source="test_good_source",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert good.id == "test_good_id"
    assert good.name == "test_good_name"
    assert good.description == "test_good_description"
    assert good.price == 100
    assert good.currency == "RUB"
    assert good.images == ["test_good_image_1", "test_good_image_2"]
    assert good.url == "test_good_url"
    assert good.source == "test_good_source"
    assert isinstance(good.created_at, datetime)
    assert isinstance(good.updated_at, datetime)


def test_good_from_dict():
    good = Good(
        **{
            "id": "test_good_id",
            "name": "test_good_name",
            "description": "test_good_description",
            "price": 100,
            "currency": "RUB",
            "images": ["test_good_image_1", "test_good_image_2"],
            "url": "test_good_url",
            "source": "test_good_source",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )

    assert good.id == "test_good_id"
    assert good.name == "test_good_name"
    assert good.description == "test_good_description"
    assert good.price == 100
    assert good.currency == "RUB"
    assert good.images == ["test_good_image_1", "test_good_image_2"]
    assert good.url == "test_good_url"
    assert good.source == "test_good_source"
    assert isinstance(good.created_at, datetime)
    assert isinstance(good.updated_at, datetime)


def test_good_to_dict():
    good = Good(
        id="test_good_id",
        name="test_good_name",
        description="test_good_description",
        price=100,
        currency="RUB",
        images=["test_good_image_1", "test_good_image_2"],
        url="test_good_url",
        source="test_good_source",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    good_dict = good.model_dump()
    assert good_dict["id"] == "test_good_id"
    assert good_dict["name"] == "test_good_name"
    assert good_dict["description"] == "test_good_description"
    assert good_dict["price"] == 100
    assert good_dict["currency"] == "RUB"
    assert good_dict["images"] == ["test_good_image_1", "test_good_image_2"]
    assert good_dict["url"] == "test_good_url"
    assert good_dict["source"] == "test_good_source"
    assert isinstance(good_dict["created_at"], datetime)
    assert isinstance(good_dict["updated_at"], datetime)
