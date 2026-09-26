# RecallGuard architecture
Revision: 2026-09-26. Implemented local core.

## Request boundary
Browser playground or API client -> Flask validation -> API-key authentication -> owner identity.

## Policy boundary
MemoryService -> consent and sensitive-pattern admission -> exact duplicate check -> shared normalized embedding encoder -> owner-scoped MemoryStore -> Chroma persistent collection.

## Retrieval boundary
Owner-scoped active IDs -> semantic candidates -> similarity or exact-term coverage -> confidence/type filters -> multi-signal ranking -> bounded serialized context -> local Ollama.

## Maintenance boundary
Separate worker/one-shot -> per-owner expiry purge -> duplicate consolidation -> low-confidence cleanup -> content-free summary.

## Test boundary
App factory and injectable dependencies -> temporary Chroma databases -> deterministic or real embedding encoder -> mock or real Ollama. Existing user storage is never selected by test runners.

## Core invariants
Owner identity cannot come from request JSON. Every object operation requires owner identity. Expired records do not enter candidates. Privacy admission runs before embeddings. Correction replaces old content. Deletion removes source record/vector. Context reserves instructions/envelope and output budget.

## Deferred public architecture
Render, Supabase and Groq are selected future providers, not implemented adapters in this revision. The container package runs the local stack with a durable volume and host Ollama; it is not claimed to fit Render free memory.
