"""Lazy storage creation; import never opens the user's database."""
from config import CHROMA_DB_PATH


def get_collection(name="conversation_memory", path=None):
    import chromadb
    client = chromadb.PersistentClient(path=str(path or CHROMA_DB_PATH))
    return client.get_or_create_collection(name=name, embedding_function=None)
