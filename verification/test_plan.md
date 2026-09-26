# Current verification plan
Run commands are in README. All automated writes use temporary storage.

1. Storage: ownership, actual record/vector deletion, corrections, UTC expiry boundary, reopened persistence.
2. Service: privacy before embeddings, exact duplicates, consent, retrieval confidence/type isolation, maintenance idempotence.
3. API: authentication, foreign ID access, invalid JSON/types/ranges, body bounds, dependency errors and partial chat success.
4. Context: complete rendered prompt budget with output/envelope reserves, oversized query rejection, skipping oversized memories, Unicode.
5. Contract mutation: intentionally break isolation, confidence and deletion and require the reusable verifier to fail each case.
6. Benchmark: identical baseline/improved scenarios with lexical and MiniLM encoders; report all misses.
7. Live: real MiniLM + Ollama through Flask, recall then explicit correction then deletion.
8. UI: browser walkthrough of key entry, save/search/edit/delete and error states.
9. Deployment: startup/health check, persistence across restart, production WSGI, secret handling and cloud resource limits.

The implementation author's test run is not independent sign-off. A reviewer must run these checks against the handbook and inspect the tests, not accept a PASS heading.
