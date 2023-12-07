import pytest
from ml.embeddings.image import get_embeddings as get_image_embeddings
from ml.embeddings.text import get_embeddings as get_text_embeddings

    
def test_image_embedding():
    embeddings = get_image_embeddings()
    image_url = "https://images-na.ssl-images-amazon.com/images/I/51Zymoq7UnL._AC_SY400_.jpg"
    result = embeddings.get_embedding(image_url)
    assert len(result) == embeddings.size
    
def test_text_embedding():
    embeddings = get_text_embeddings()
    text = "Test Text"
    result = embeddings.get_embedding(text)
    assert len(result) == embeddings.size