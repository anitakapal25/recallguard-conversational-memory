# Handbook gap ledger — 2026-09-26
This is a present-state ledger, not evidence of historical work.

| Deliverable | Current evidence | Remaining |
|---|---|---|
| 1 reconstruction | Existing problem/failure/principles documents | Source-specific citations; approved required formats |
| 2 weekly research | Existing week-1 notes | Broad component scan, source evidence, recorded actual review/challenges; no fabricated presentation |
| 3 baseline | Runnable baseline + fixed JSONL + actual lexical/semantic CSV/error outputs | Larger held-out data, generated-response quality, model-token and index-growth measurements |
| 4 design | Updated API/schema/threat model, ADR-005/006 and rendered design PDFs | Expand scale/recovery design |
| 5 Genesis | Existing scaffold, new current implementation work | Actual independent verification and checkpoint/recovery evidence; do not backdate loops |
| 6 implementation | Owner-scoped CRUD, privacy admission, expiry, maintenance, bounded context, isolated tests | Held-out semantic evaluation, live adversarial testing, public deployment and independent release review |
| 7 journal | Historical notes plus new revision record | Student review/defense and subsequent real work-session entries |
| 8 transfer/contribution | Transfer study, public-interface contract with positive controls and mutation tests | External review of transfer/contribution |

Core limitations: rule-based extraction; explicit correction instead of automatic conflict resolution; heuristic confidence; conservative byte budget instead of model-exact tokenizer; API-key authentication instead of managed accounts.
