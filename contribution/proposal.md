# Reusable Contribution Proposal: Memory Verification Contract

## Problem
Memory systems can pass happy-path tests while still allowing cross-user leakage, low-confidence results, deleted memories, wrong memory types, or persistent test contamination.

## Evidence
RecallGuard development exposed retrieval failures involving persistent collections, confidence filtering and user isolation. The final tests required isolated collections and explicit behavioral checks.

## Design
Create `verify_memory_contract.py`, a reusable behavioral verification tool. It checks:
1. User isolation
2. Deleted-memory exclusion
3. Confidence filtering
4. Memory-type filtering
5. Top-k bounds
6. Empty-user behavior
7. Similarity ordering

The checks use the public MemoryStore/MemoryRetriever behavior rather than ChromaDB internals, so the contract can be reused with another vector store.

## Trade-offs
**Benefits:** reusable, catches security/correctness regressions, tests the memory boundary, and supports backend replacement.
**Costs:** adds a verification step and cannot validate every domain-specific policy.

## Acceptance criteria
- All seven checks pass on RecallGuard.
- A deliberately broken isolation implementation is detected.
- A deliberately broken confidence filter is detected.
- Deleted-memory leakage is detected.
- The tool runs independently of Flask.
- Output identifies every passed/failed check.
- Checks depend on public memory interfaces, not ChromaDB internals.

## Contribution value
This turns implementation failures into a reusable engineering verification workflow for memory systems and long-running agents.
