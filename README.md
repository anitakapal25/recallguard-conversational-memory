# RecallGuard
A local conversational-memory service with a Flask playground, owner-scoped Chroma storage, explicit correction, deletion, retention, and reproducible verification.

## Current status
This revision implements the handbook's core memory paths. It is **not a completed eight-deliverable submission or a verified public production deployment**.
See [current verification](verification/results/current_verification.md) and [handbook gap ledger](verification/handbook_gap_ledger.md).
Historical PASS reports predate this revision and are not current release approval.

## Setup
Use Python 3.12+ in a virtual environment. The recorded local checks use Python 3.14.4.
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```
Download MiniLM on first application startup. Install Ollama separately and run:
```powershell
ollama pull llama3.2:3b
```
Configure non-shared keys outside source. Generate each value with `python -c "import secrets; print(secrets.token_hex(32))"`.
```powershell
$env:RECALLGUARD_API_KEYS='{"replace-with-random-key":"your-user-id"}'
$env:RECALLGUARD_DB_PATH='C:\recallguard-data'
python implementation/app.py
```
Open http://127.0.0.1:5000 and enter your key. A missing key map denies all memory routes.
The browser keeps the key only in the page, not localStorage. Do not deploy example credentials.
Explicit POST/PUT writes require `consent:true`; chat only stores extracted facts with `remember:true`.
Automatic contradiction resolution is **not implemented**: use Edit to explicitly replace a fact. The old content/vector is replaced rather than retained in a history table.

## Production server, local deployment
```powershell
$env:PYTHONPATH='implementation'
waitress-serve --host=127.0.0.1 --port=5000 --call app:create_app
```
Use one application process for the in-process write lock. TLS, rate limits, account/key provisioning and public cloud configuration remain deployment gates.
Do not put the Chroma directory on ephemeral cloud storage. The existing root database is never migrated by tests.
Default CLI binding is localhost and debug mode is disabled.

## Background maintenance
Run in a separate supervised process or invoke `--once` hourly with your OS scheduler:
```powershell
python implementation/maintenance.py --once
python implementation/maintenance.py --interval 3600
```
Expired records are excluded on every read, even if the worker is stopped. The worker physically removes expired/legacy-deleted records and consolidates exact duplicates.
Do not overlap workers. Cross-process mutation transactions are not provided by this prototype.

## Verification
```powershell
python -m pytest -q --junitxml=verification/results/core-tests.xml
python contribution/verify_memory_contract.py
python verification/run_evaluation.py
python verification/run_evaluation.py --semantic
python verification/live_smoke.py
```
The normal suite uses **real temporary Chroma databases** and deterministic embeddings; no model downloads or LLM calls.
The semantic benchmark uses MiniLM. The live smoke additionally requires Ollama.
Benchmark output is under `verification/results/offline/` and `semantic/`. Inspect failures, not just totals.
Both systems receive the same fixed scenarios. The baseline retains all candidate text, ranks by similarity, and has no lifecycle/context policy.
UTF-8 byte counts are conservative prompt-budget units, not exact model-token measurements.
The benchmark is a small development suite, not a held-out generalization claim.

## API
All memory routes require `X-API-Key`. User identity comes only from the server key map.
- GET /health: process liveness.
- GET /ready: database availability; does not claim LLM readiness.
- POST /memory: explicit write (`text, consent, memory_type?, importance?, confidence?, retention_days?`).
- GET /memories and GET /memory/<id>: active owner-scoped records.
- PUT /memory/<id>: explicit correction (`text, consent`); keeps expiry and increments version.
- DELETE /memory/<id>: remove record and vector; unknown/foreign IDs return 404.
- POST /retrieve: `query, top_k?` (1-20).
- POST /context: `query`; bounded prompt and budget statistics.
- POST /chat: `message, remember?, conversation_id?`.
- POST /reflection: maintenance for the authenticated user.

400 invalid input; 401 unauthenticated; 404 unknown/foreign ID; 413 body too large; 503 dependency failure.
A chat 503 can include **successful memory writes**: inspect `stored_memories` before retrying.
Exact duplicates are idempotent within a single process; arbitrary request-level idempotency is not promised.

## Data handling and limits
- Supported email/phone/card/Aadhaar/PAN/credential patterns are rejected at the service boundary before embeddings and inference. This is not complete PII detection.
- New records expire after at most seven days. Legacy records without expiry retain their previous behavior until explicitly managed; no silent migration.
- Deletion removes logical records through Chroma. It does not promise forensic erasure of SQLite pages, external backups, old logs, or previously exported results.
- Metadata carries source, conversation reference, UTC timestamps and version. It does not retain original unredacted transcripts.
- Operational logs contain request IDs/status/timing, not message text or provider exception details.
- Readiness, storage, correction and deletion do not depend on Ollama.
- Candidate search scans active IDs before query; scale beyond a small demo requires indexed expiry filtering.
- Ranking coefficients and relevance threshold remain hypotheses. Hybrid retrieval also admits candidates containing every meaningful query term. Small development-suite results do not establish generalization.
- Prompt data is serialized and separated from system instructions, but no universal prompt-injection resistance is claimed.

## Handbook evidence
The original reconstruction/research/transfer documents remain available. New results and decisions are dated honestly; missing historical reviews or Genesis checkpoints are not fabricated.
See `design/decision_records/ADR-005-handbook-core-hardening.md` for decisions and alternatives.
