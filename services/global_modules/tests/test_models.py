from global_modules.models import Good, GoodEmbedding


import pytest
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl as URL
from global_modules.models.good import Good

def test_good_creation():
    good = Good(
        id=1,
        name="Test Good",
    )
    assert isinstance(good, Good)

def test_good_with_arguments():
    good = Good(
        id=1,
        name="Test Good",
    )
    assert good.id == 1
    assert good.name == "Test Good"
    # Add more assertions for each attribute

def test_good_field_types():
    good = Good(
        id=1,
        name="Test Good",
    )
    assert isinstance(good.id, int)
    assert isinstance(good.name, str)
    # Add more assertions for each attribute
    
def test_good_transferred():
    good = Good(
        id=1,
        name="Test Good",
        description="Test Description",
        price=1.0,
        images=["https://example.com/image.jpg"],
        source="Test Source",
        url="https://example.com",
        rating=1.0,
        reviews=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    good_json = good.model_dump_json()
    
    assert isinstance(good_json, str)
    
    good_loaded = Good.model_validate_json(good_json)
    
    assert isinstance(good_loaded, Good)
    assert isinstance(good_loaded.id, int)
    assert isinstance(good_loaded.name, str)
    
    assert good_loaded.id == good.id
    assert good_loaded.name == good.name
    assert good_loaded.description == good.description
    assert good_loaded.price == good.price
    assert good_loaded.images == good.images
    assert good_loaded.source == good.source
    assert good_loaded.url == good.url
    assert good_loaded.rating == good.rating
    assert good_loaded.reviews == good.reviews
    assert good_loaded.created_at == good.created_at
    assert good_loaded.updated_at == good.updated_at
    # Add more assertions for each attribute

import numpy as np
from global_modules.models.good import GoodEmbedding

def test_good_embedding_creation():
    good_embedding = GoodEmbedding(id=1, vector=np.array([1, 2, 3]))
    assert isinstance(good_embedding, GoodEmbedding)

def test_good_embedding_with_arguments():
    vector = np.array([1, 2, 3])
    good_embedding = GoodEmbedding(id=1, vector=vector)
    assert good_embedding.id == 1
    assert np.array_equal(good_embedding.vector, vector)

def test_good_embedding_field_types():
    vector = np.array([1, 2, 3])
    good_embedding = GoodEmbedding(id=1, vector=vector)
    assert isinstance(good_embedding.id, int)
    assert isinstance(good_embedding.vector, np.ndarray)
    
def test_good_embedding_transferred():
    vector = np.array([1, 2, 3])
    good_embedding = GoodEmbedding(id=1, vector=vector)
    good_embedding_dict = good_embedding.model_dump()
    
    assert isinstance(good_embedding_dict, dict)
    
    good_embedding_loaded = GoodEmbedding.model_validate(good_embedding_dict)
    
    assert isinstance(good_embedding_loaded, GoodEmbedding)
    assert isinstance(good_embedding_loaded.id, int)
    assert isinstance(good_embedding_loaded.vector, np.ndarray)
    
    assert good_embedding_loaded.id == good_embedding.id
    assert np.array_equal(good_embedding_loaded.vector, good_embedding.vector)
