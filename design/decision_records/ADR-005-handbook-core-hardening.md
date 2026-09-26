# ADR-005: Verify the existing memory core before cloud migration
Status: accepted for the local core revision
Date: 2026-09-26

## Context and evidence
The handbook requires runnable baseline evidence, isolation/deletion tests, bounded context and lifecycle management.
The earlier delete route did not pass ownership; PII filtering was unused; tests shared the persistent database; reports overstated verification.

## Decision
Retain Flask, Chroma and local Ollama. Introduce an injectable application/service boundary, temporary real-database tests, owner-required CRUD, explicit corrections and seven-day retention for new records.
Use exact deduplication in admission: embedding similarity alone cannot distinguish a duplicate from a changed or negated preference.
Replace corrected text/vector in place, preserving ID/provenance/expiry and incrementing version. Do not retain content history.
Use a conservative UTF-8 byte prompt budget with system-envelope and output reserves. This is labeled as a bound, not exact tokenization.
Use one embedding model per service instance with normalized outputs.
Keep generation failures distinct from committed memory operations.

## Alternatives
A Supabase/provider migration helps eventual cloud deployment but increases scope before core invariants are verified.
Automatic LLM conflict resolution is deferred: unverified model decisions should not silently overwrite memory.
Soft deletion alone does not meet the handbook's source-storage deletion gate; physical API deletion is used.
No schema rewrite or destructive migration of the existing user database occurs.

## Validation and tradeoffs
Run API/storage regressions, mutation checks, lexical and real-embedding benchmarks, and live Ollama smoke tests.
Active-ID filtering is simple and testable but O(n) per user. Cross-process write transactions and exact model-token counts remain future work.
Revisit storage/index design when measured scale or public deployment constraints justify it.
