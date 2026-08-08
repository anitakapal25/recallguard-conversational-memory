# Reusable memory verification contract
import uuid
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from memory_store import MemoryStore
from retrieval import MemoryRetriever

MODEL = SentenceTransformer(EMBEDDING_MODEL)

def embed(text):
    return MODEL.encode(text).tolist()

def run_contract_checks(store, retriever):
    a, b = "contract_user_a", "contract_user_b"
    checks = []
    def check(name, condition):
        checks.append((name, bool(condition)))

    store.add_memory(a, "coffee", embed("coffee"))
    store.add_memory(b, "football", embed("football"))
    check("user_isolation", retriever.retrieve("football", a) == [])

    store.add_memory(a, "uncertain", embed("uncertain"), confidence=0.2)
    results = retriever.retrieve("uncertain", a, min_confidence=0.5)
    check("confidence_filter", all(r["metadata"].get("confidence", 0) >= 0.5 for r in results))

    store.add_memory(a, "likes tea", embed("likes tea"), memory_type="preference")
    results = retriever.retrieve_preferences(a)
    check("type_filter", all(r["metadata"].get("memory_type") == "preference" for r in results))

    check("top_k_bound", len(retriever.retrieve("coffee", a, top_k=1)) <= 1)
    check("empty_user", retriever.retrieve("anything", "unknown_user") == [])

    results = retriever.retrieve("coffee", a, top_k=10)
    scores = [r["similarity"] for r in results]
    check("similarity_ordering", scores == sorted(scores, reverse=True))

    memory_id = store.add_memory(a, "temporary", embed("temporary"))
    store.delete_memory(memory_id)
    results = retriever.retrieve("temporary", a)
    check("deleted_memory_exclusion", all(r["id"] != memory_id for r in results))

    return {"passed": sum(x for _,x in checks), "total": len(checks),
            "checks": [{"name":n,"passed":ok} for n,ok in checks]}

def main():
    store = MemoryStore(collection_name=f"verification_{uuid.uuid4().hex}")
    result = run_contract_checks(store, MemoryRetriever(store))
    for c in result["checks"]:
        print(f"[{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
    print(f"\n{result['passed']}/{result['total']} checks passed.")
    if result["passed"] != result["total"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
