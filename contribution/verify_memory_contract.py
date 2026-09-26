"""Reusable, positive-and-negative memory contract. All state is caller-owned."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/"implementation"), str(ROOT)]
from verification.support import HashEncoder


def run_contract_checks(store, retriever):
    encoder = retriever.model
    checks = []
    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
    own = store.add_memory("contract-a", "coffee", encoder.encode("coffee"))
    other = store.add_memory("contract-b", "coffee", encoder.encode("coffee"))
    results = retriever.retrieve("coffee", "contract-a")
    check("user_isolation", any(r["id"] == own for r in results) and all(r["id"] != other for r in results))
    low = store.add_memory("contract-a", "coffee uncertain", encoder.encode("coffee uncertain"), confidence=.1)
    results = retriever.retrieve("coffee", "contract-a", min_confidence=.5)
    check("confidence_filter", any(r["id"] == own for r in results) and all(r["id"] != low for r in results))
    pref = store.add_memory("contract-a", "tea", encoder.encode("tea"), memory_type="preference")
    results = retriever.retrieve_preferences("contract-a")
    check("type_filter", any(r["id"] == pref for r in results) and all(r["metadata"]["memory_type"] == "preference" for r in results))
    check("top_k_bound", len(retriever.retrieve("coffee", "contract-a", top_k=1)) == 1)
    check("empty_user", retriever.retrieve("coffee", "unknown") == [])
    results = retriever.retrieve("coffee", "contract-a", top_k=10)
    scores = [r["similarity"] for r in results]
    check("similarity_ordering", bool(scores) and scores == sorted(scores, reverse=True))
    store.delete_memory(own, "contract-a")
    check("deleted_memory_exclusion", not store.get_memory(own, "contract-a")["ids"]
          and all(r["id"] != own for r in retriever.retrieve("coffee", "contract-a")))
    return {"passed": sum(c["passed"] for c in checks), "total": len(checks), "checks": checks}


if __name__ == "__main__":
    import json
    import tempfile
    import chromadb
    from chromadb.config import Settings
    from memory_store import MemoryStore
    from retrieval import MemoryRetriever
    with tempfile.TemporaryDirectory(prefix="recallguard-contract-") as path:
        client = chromadb.PersistentClient(path=path,settings=Settings(anonymized_telemetry=False))
        collection = client.create_collection("contract_memory",embedding_function=None)
        store = MemoryStore(collection=collection)
        result = run_contract_checks(store,MemoryRetriever(store,HashEncoder()))
        client.delete_collection("contract_memory")
        client._system.stop()
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["passed"] == result["total"] else 1)
