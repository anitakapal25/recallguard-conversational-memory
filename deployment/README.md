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
The user selected Render + Supabase + Groq for a future free public deployment. This local Chroma/Ollama container is not presented as that implementation.
Before public deployment:
1. Obtain non-secret account/project setup status and configure secrets through provider secret stores.
2. Implement and test the Supabase storage/auth adapter and Groq provider with the same contract suite.
3. Verify an embedding runtime within the selected host's memory limit (current PyTorch stack is not assumed to fit a 512 MB free instance).
4. Add per-account rate/quota limits, public TLS and backup/restore evidence.
5. Run clean install/container and real deployed smoke tests, including persistence across restart.
6. Obtain independent release review against the handbook requirements.

No public deployment was made. No cloud credentials were requested in chat or committed.
