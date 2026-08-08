"""
test_retrieval.py

Unit tests for retrieval.py
"""

import pytest
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL
from memory_store import MemoryStore
from retrieval import MemoryRetriever
import uuid
import pytest


MODEL = SentenceTransformer(EMBEDDING_MODEL)


@pytest.fixture
def store():
    return MemoryStore(
        collection_name=f"test_{uuid.uuid4().hex}"
    )


@pytest.fixture
def retriever(store):
    return MemoryRetriever(store)


@pytest.fixture
def user():
    return "retrieval_test_user"


def embed(text):
    return MODEL.encode(text).tolist()


# --------------------------------------------------
# Basic Retrieval
# --------------------------------------------------

def test_basic_retrieval(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "I like coffee.",
        embed("I like coffee."),
        memory_type="preference",
    )

    results = retriever.retrieve(
        query="coffee",
        user_id=user,
    )

    assert len(results) >= 1
    assert "coffee" in results[0]["content"].lower()


# --------------------------------------------------
# Top K
# --------------------------------------------------

def test_top_k(
    store,
    retriever,
    user,
):

    for i in range(10):

        store.add_memory(
            user,
            f"Memory {i}",
            embed(f"Memory {i}"),
        )

    results = retriever.retrieve(
        "Memory",
        user,
        top_k=5,
    )

    assert len(results) <= 5


# --------------------------------------------------
# Preference Filter
# --------------------------------------------------

def test_preference_filter(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "I like pizza.",
        embed("I like pizza."),
        memory_type="preference",
    )

    store.add_memory(
        user,
        "Paris is in France.",
        embed("Paris is in France."),
        memory_type="fact",
    )

    results = retriever.retrieve_preferences(
        user
    )

    assert len(results) > 0

    for memory in results:

        assert (
            memory["metadata"]["memory_type"]
            == "preference"
        )


# --------------------------------------------------
# Fact Filter
# --------------------------------------------------

def test_fact_filter(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "Earth has one moon.",
        embed("Earth has one moon."),
        memory_type="fact",
    )

    results = retriever.retrieve_facts(
        user
    )

    assert len(results) >= 1

    assert (
        results[0]["metadata"]["memory_type"]
        == "fact"
    )


# --------------------------------------------------
# Task Filter
# --------------------------------------------------

def test_task_filter(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "Meeting tomorrow at 10.",
        embed("Meeting tomorrow at 10."),
        memory_type="task",
    )

    results = retriever.retrieve_tasks(
        user
    )

    assert len(results) >= 1

    assert (
        results[0]["metadata"]["memory_type"]
        == "task"
    )


# --------------------------------------------------
# Confidence Filter
# --------------------------------------------------

def test_confidence_filter(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "Low confidence",
        embed("Low confidence"),
        confidence=0.20,
    )

    results = retriever.retrieve(
        "confidence",
        user,
        min_confidence=0.5,
    )

    assert len(results) == 0


# --------------------------------------------------
# User Isolation
# --------------------------------------------------

def test_user_isolation(
    store,
    retriever,
):

    store.add_memory(
        "user1",
        "Coffee",
        embed("Coffee"),
    )

    store.add_memory(
        "user2",
        "Football",
        embed("Football"),
    )

    results = retriever.retrieve(
        "Football",
        "user1",
    )

    assert len(results) == 0


# --------------------------------------------------
# Empty Search
# --------------------------------------------------

def test_empty_search(
    retriever,
):

    results = retriever.retrieve(
        "Nothing",
        "unknown_user",
    )

    assert isinstance(
        results,
        list,
    )

    assert len(results) == 0


# --------------------------------------------------
# Similarity Ordering
# --------------------------------------------------

def test_similarity_order(
    store,
    retriever,
    user,
):

    store.add_memory(
        user,
        "I love coffee.",
        embed("I love coffee."),
    )

    store.add_memory(
        user,
        "I like tea.",
        embed("I like tea."),
    )

    results = retriever.retrieve(
        "coffee",
        user,
    )

    assert len(results) > 0

    similarities = [
        memory["similarity"]
        for memory in results
    ]

    assert similarities == sorted(
        similarities,
        reverse=True,
    )