# Deployment gates
## Local verified paths
The Flask API is exercised by isolated API tests and real MiniLM/Ollama smoke verification.
The browser harness uses Waitress on 127.0.0.1:5055 with synthetic data and deterministic generation; it is not the public deployment.

## Container package
Dockerfile and compose.yaml retain the core Chroma/Ollama stack. Compose binds to localhost, persists Chroma in a named volume, and requires a private API-key environment mapping.
Start Docker, set RECALLGUARD_API_KEYS, ensure the host Ollama endpoint is reachable, then run:
```
docker compose up --build
```
The first embedding download needs network access. Build/start/restart tests have NOT been run because Docker's daemon was unavailable during this revision.
Do not run docker compose down -v unless you intend to delete stored data.

## Public deployment — pending
The user selected Render + Supabase + Groq for a free public deployment. Use `render.yaml` and `requirements-cloud.txt`, not the local Chroma/Ollama Dockerfile, for that deployment.

The cloud adapter uses normalized MiniLM ONNX embeddings and exact squared-distance searches over PostgreSQL arrays. This is deliberately limited to a small demonstration (500 memories per owner, 5,000 total); it is not a scalable vector-index implementation. Do not mix these embeddings with an existing local index. The dedicated Supabase schema is in `supabase.sql`; anonymous and authenticated browser roles have no access. Only the trusted API's service role can call its functions. API keys still determine user identity; managed GitHub login is not included in this first deployment.

Configure `SUPABASE_SERVICE_ROLE_KEY`, `GROQ_API_KEY`, and a private `RECALLGUARD_API_KEYS` JSON map only in Render's secret environment settings. Never place provider keys in the frontend. The UI explains cloud data destinations. Free plan selection alone does not guarantee no charges on a Render workspace with a payment method: bandwidth/build overages can still be billed. Do not deploy until the workspace cost choice is resolved.

Request limits: 60 API calls/minute per owner, 5 chat calls/minute per owner, 200 chat calls/day globally per running process. Limits reset on process restart and are demo abuse controls, not a financial guarantee. Supabase enforces storage quotas transactionally and purges expired rows during insert; otherwise expiry is filtered on read and maintenance can delete it. Scheduled cleanup remains follow-up work.

Verification: 59 automated tests passed, including mocked cloud transports and rate limits. The actual Supabase schema and a rolled-back SQL transaction verified isolation, correction, vector retrieval, expiry, deletion and anonymous denial. FastEmbed produced a normalized 384-dimensional vector in an isolated Python 3.12 environment. A live REST/provider integration test, Render memory fit and deployed restart/persistence smoke are still required.
Before public deployment:
1. Obtain non-secret account/project setup status and configure secrets through provider secret stores.
2. Run real REST and Groq integration checks after credentials are configured; managed account auth remains deferred.
3. Verify an embedding runtime within the selected host's memory limit (current PyTorch stack is not assumed to fit a 512 MB free instance).
4. Add per-account rate/quota limits, public TLS and backup/restore evidence.
5. Run clean install/container and real deployed smoke tests, including persistence across restart.
6. Obtain independent release review against the handbook requirements.

No public deployment was made. No cloud credentials were requested in chat or committed.
