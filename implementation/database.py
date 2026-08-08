"""
database.py

ChromaDB connection utilities.
"""

import chromadb
from config import CHROMA_DB_PATH

client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)


def get_collection(
    name: str = "conversation_memory",
):
    return client.get_or_create_collection(
        name=name
    )