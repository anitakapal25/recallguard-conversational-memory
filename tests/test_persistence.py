import chromadb
from chromadb.config import Settings
from memory_store import MemoryStore
from verification.support import HashEncoder


def test_persists_when_store_reopened(tmp_path):
    path=str(tmp_path/"persistent")
    client=chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
    collection=client.create_collection("persistent_memory",embedding_function=None)
    store=MemoryStore(collection=collection)
    mid=store.add_memory("alice","I prefer coffee",HashEncoder().encode("I prefer coffee"))
    reopened=MemoryStore(collection=client.get_collection("persistent_memory",embedding_function=None))
    assert reopened.get_memory(mid,"alice")["documents"]==["I prefer coffee"]
    assert reopened.get_memory(mid,"bob")["ids"]==[]
    client.delete_collection("persistent_memory")
