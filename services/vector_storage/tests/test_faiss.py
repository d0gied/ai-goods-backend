import numpy as np
import pytest
from vector_storage.repositories.faiss import FaissRepository
from vector_storage.models import GoodEmbedding
import shutil

@pytest.fixture
def faiss_repo():
    repo = FaissRepository(path="./tests/faiss.db", size=5)
    repo.add([
        GoodEmbedding(id=1, vector=np.array([0.1, 0.2, 0.3, 0.4, 0.5])),
        GoodEmbedding(id=2, vector=np.array([0.2, 0.3, 0.4, 0.5, 0.6])),
        GoodEmbedding(id=3, vector=np.array([0.3, 0.4, 0.5, 0.6, 0.7])),
        GoodEmbedding(id=4, vector=np.array([0.4, 0.5, 0.6, 0.7, 0.8])),
        GoodEmbedding(id=5, vector=np.array([0.5, 0.6, 0.7, 0.8, 0.9])),
        GoodEmbedding(id=6, vector=np.array([0.6, 0.7, 0.8, 0.9, 1.0])),
    ])
    return repo

@pytest.fixture
def good_embedding():
    return GoodEmbedding(id=1, vector=np.array([0.1, 0.2, 0.3, 0.4, 0.5]))

def test_add(faiss_repo):
    assert faiss_repo.faiss.ntotal == 6

def test_search_without_threshold(faiss_repo, good_embedding):
    result = faiss_repo.search(good_embedding, k=5)
    assert isinstance(result, list)
    assert len(result) <= 5

def test_search_with_threshold(faiss_repo, good_embedding):
    result = faiss_repo.search(good_embedding, k=5, threshold=0.5)
    assert isinstance(result, list)
    assert len(result) <= 5
    for id in result:
        assert isinstance(id, int)
    for id in result:
        assert id in [1, 2, 3, 4]

def test_save_load(faiss_repo):
    faiss_repo.save()
    assert faiss_repo.path.exists()
    
    new_repo = FaissRepository(path=faiss_repo.path, size=faiss_repo.size)
    new_repo.load()
    
    assert new_repo.faiss.ntotal == 6
    
    shutil.rmtree(new_repo.path.parent)