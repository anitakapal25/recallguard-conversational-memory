"""Isolated real Chroma storage and deterministic embeddings. No model downloads."""
import pytest
import chromadb
from chromadb.config import Settings
from memory_store import MemoryStore
from service import MemoryService
from app import create_app
from verification.support import HashEncoder


@pytest.fixture
def store(tmp_path):
    client = chromadb.PersistentClient(path=str(tmp_path / "chroma"), settings=Settings(anonymized_telemetry=False))
    collection = client.create_collection("test_memory", embedding_function=None)
    yield MemoryStore(collection=collection)
    client.delete_collection("test_memory")


@pytest.fixture
def encoder():
    return HashEncoder()


@pytest.fixture
def service(store, encoder):
    return MemoryService(store, encoder)


@pytest.fixture
def client(service):
    application = create_app(service, {"test-a": "alice", "test-b": "bob"})
    application.config["TESTING"] = True
    return application.test_client()
