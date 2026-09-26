# Threat model and limits
Untrusted boundaries: browser/API input, retrieved text, embeddings/model dependencies and LLM responses.
Trusted boundary: server-side API-key mapping and local storage administration.

| Threat | Implemented control | Evidence / residual risk |
|---|---|---|
| Cross-user object access | Owner filters on reads/updates/deletes/search | API and storage regression tests; malformed IDs indistinguishable from foreign IDs |
| Shared browser credential | User-entered key, no hard-coded key, no browser persistence | UI source and authenticated tests; production identity/key rotation still needed |
| Sensitive-content retention | Pattern rejection before embed/store/inference | Positive/negative tests; pattern coverage is incomplete |
| Stale or deleted recall | Explicit correction, read-time expiry, physical API deletion | Real database tests; no forensic/backup erasure promise |
| Prompt injection | Serialized memory data plus separate system instructions | Serialization tests only; live adversarial model evaluation remains open |
| Error/log disclosure | Generic errors, content-free request logs | Injected exception tests |
| Unbounded work | Text/body/top-k/output limits; model timeout | Validation tests; public rate limiting still required |
| Stored XSS | textContent-based UI; restrictive CSP | UI review; no untrusted HTML renderer |
| Test contamination | Temporary database fixtures | No default database used by test/evaluation commands |

Deployment boundary: local single-process service. Public TLS, quotas, external identity, backups and recovery must be validated before public production use.
