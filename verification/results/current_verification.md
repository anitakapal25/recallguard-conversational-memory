# RecallGuard: current verification
Generated: 2026-09-26T07:48:44.392644+00:00
Status: verified local core checks; independent review and public deployment pending.

## Automated regression
52 tests recorded; 0 failures/errors. Source: core-tests.xml.
Coverage: object ownership, actual deletion, correction/provenance, expiry boundary, privacy positive/negative cases, consent, context budget, malformed API inputs, persistence, dependency failures and contract mutation.
The reusable verifier passes 7 checks and its tests detect deliberately broken isolation, confidence and deletion implementations.

## Corrected baseline comparison
Dataset SHA-256: 33d83f5caa7af18c27d9c7b9564fda8d53d87797c166b37b2acbccff0c8df530
MiniLM: baseline 4/16; improved 16/16.
Lexical test encoder: baseline 4/16; improved 16/16.
Seven retrieval calls per case; p50/p95 and first-query milliseconds, retained content bytes and prompt UTF-8 units are in comparison.csv. These are not LLM latency, disk index size or exact model-token counts.
This is a development/regression suite used during implementation, not a held-out generalization claim.

## Benchmark correction
An earlier generated long-context fixture incorrectly contained NaN rather than repeated text. It was corrected and a regression assertion added. Earlier pre-hybrid outputs are retained as superseded, not as valid before/after measurements.

## Real model smoke
Status: passed. Model: llama3.2:3b.
Initial response: You prefer Python for programming.
After explicit correction: You prefer Rust for programming.
The smoke also verified deletion. One synthetic scenario is not broad response-quality evidence.

## UI and deployment checks
Waitress test server starts on loopback. Browser verified consented storage, provenance/expiry display and request inspector using synthetic data and a deterministic generation stub. JavaScript syntax checked.
A native prompt blocked automation; controls were changed to inline confirmations. The full revised browser walkthrough remains pending.
Docker daemon was unavailable, so container build/start/restart is unverified. Dockerfile, Compose and deployment instructions are provided. No public service was deployed.

## Residual risks and remaining handbook evidence
Independent specification-based review remains outstanding. Existing historical PASS reports are not release sign-off.
Automatic contradiction resolution, calibrated confidence, exact model tokenization, broad prompt-injection evaluation, generated-response benchmarks, held-out data, public quotas/identity/TLS, backup recovery and cloud adapters remain open.
Pattern-based PII admission is limited. Physical API deletion does not promise forensic disk or external-backup erasure.
Original reconstruction/research/transfer work remains; missing presentations and historical checkpoints were not fabricated.

## Reproduce
python -m pytest -q --junitxml=verification/results/core-tests.xml
python contribution/verify_memory_contract.py
python verification/run_evaluation.py
python verification/run_evaluation.py --semantic
python verification/live_smoke.py
