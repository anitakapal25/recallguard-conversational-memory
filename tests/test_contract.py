import pytest
from contribution.verify_memory_contract import run_contract_checks
from retrieval import MemoryRetriever


def test_contract_passes(store, encoder):
    result = run_contract_checks(store, MemoryRetriever(store, encoder))
    assert result["passed"] == result["total"] == 7


@pytest.mark.parametrize("broken_check", ["user_isolation", "confidence_filter", "deleted_memory_exclusion"])
def test_contract_detects_broken_implementation(store, encoder, broken_check):
    retriever = MemoryRetriever(store, encoder)
    original = retriever.retrieve
    cached = []
    def broken(query, user_id, top_k=5, **kwargs):
        if broken_check == "confidence_filter":
            kwargs["min_confidence"] = 0
        result = original(query, user_id, top_k, **kwargs)
        if broken_check == "user_isolation" and user_id == "contract-a":
            result += original(query, "contract-b", top_k)
        if broken_check == "deleted_memory_exclusion" and user_id == "contract-a":
            if not cached and result:
                cached.append(result[0])
            if cached and all(r["id"] != cached[0]["id"] for r in result):
                result.append(cached[0])
        return result
    retriever.retrieve = broken
    result = run_contract_checks(store, retriever)
    checks = {c["name"]:c["passed"] for c in result["checks"]}
    assert checks[broken_check] is False
