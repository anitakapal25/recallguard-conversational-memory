"""
test_memory_store.py

Unit tests for ChromaDB MemoryStore.
"""

import uuid

import pytest
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL
from memory_store import MemoryStore

MODEL = SentenceTransformer(EMBEDDING_MODEL)


@pytest.fixture
def store():
    return MemoryStore(
        collection_name=f"test_{uuid.uuid4().hex}"
    )


@pytest.fixture
def user_id():
    return "test_user"


def embedding(text):
    return MODEL.encode(text).tolist()


# --------------------------------------------------
# Add Memory
# --------------------------------------------------

def test_add_memory(store, user_id):

    memory_id = store.add_memory(
        user_id=user_id,
        text="I like coffee.",
        embedding=embedding("I like coffee."),
        memory_type="preference",
        importance=0.8,
        confidence=0.95,
    )

    assert memory_id is not None
    assert isinstance(memory_id, str)


# --------------------------------------------------
# Retrieve Memory
# --------------------------------------------------

def test_retrieve_memory(store, user_id):

    store.add_memory(
        user_id,
        "I work remotely.",
        embedding("I work remotely."),
    )

    results = store.retrieve_memory(
        user_id,
        embedding("work remotely"),
        top_k=5,
    )

    assert len(results["documents"][0]) > 0


# --------------------------------------------------
# List Memories
# --------------------------------------------------

def test_list_memories(store, user_id):

    store.add_memory(
        user_id,
        "Python developer",
        embedding("Python developer"),
    )

    result = store.list_memories(
        user_id
    )

    assert len(result["ids"]) >= 1


# --------------------------------------------------
# Duplicate Detection
# --------------------------------------------------

def test_duplicate_detection(store, user_id):

    emb = embedding("I enjoy coffee.")

    store.add_memory(
        user_id,
        "I enjoy coffee.",
        emb,
    )

    assert store.is_duplicate(
        user_id,
        emb,
    ) is True


# --------------------------------------------------
# Delete Memory
# --------------------------------------------------

def test_delete_memory(store, user_id):

    memory_id = store.add_memory(
        user_id,
        "Temporary memory",
        embedding("Temporary memory"),
    )

    assert store.delete_memory(
        memory_id
    )

    result = store.get_memory(
        memory_id
    )

    assert result["metadatas"][0]["deleted"] is True


# --------------------------------------------------
# Update Memory
# --------------------------------------------------

def test_update_memory(store, user_id):

    memory_id = store.add_memory(
        user_id,
        "Old memory",
        embedding("Old memory"),
    )

    updated = store.update_memory(
        memory_id,
        "Updated memory",
        embedding("Updated memory"),
    )

    assert updated


# --------------------------------------------------
# User Isolation
# --------------------------------------------------

def test_user_isolation(store):

    store.add_memory(
        "user1",
        "Coffee",
        embedding("Coffee"),
    )

    store.add_memory(
        "user2",
        "Football",
        embedding("Football"),
    )

    result = store.list_memories(
        "user1"
    )

    docs = result["documents"]

    assert "Coffee" in docs
    assert "Football" not in docs


# --------------------------------------------------
# Empty Retrieval
# --------------------------------------------------

def test_empty_search(store):

    result = store.retrieve_memory(
        "unknown_user",
        embedding("Nothing"),
    )

    assert len(result["documents"][0]) == 0


# --------------------------------------------------
# Multiple Memories
# --------------------------------------------------

def test_multiple_memories(store, user_id):

    for i in range(10):

        store.add_memory(
            user_id,
            f"Memory {i}",
            embedding(f"Memory {i}"),
        )

    result = store.retrieve_memory(
        user_id,
        embedding("Memory"),
        top_k=5,
    )

    assert len(result["documents"][0]) <= 5


# --------------------------------------------------
# Memory Metadata
# --------------------------------------------------

def test_metadata(store, user_id):

    memory_id = store.add_memory(
        user_id,
        "Metadata Test",
        embedding("Metadata Test"),
        memory_type="fact",
        importance=0.9,
        confidence=0.88,
    )

    result = store.get_memory(
        memory_id
    )

    metadata = result["metadatas"][0]

    assert metadata["memory_type"] == "fact"
    assert metadata["importance"] == 0.9
    assert metadata["confidence"] == 0.88