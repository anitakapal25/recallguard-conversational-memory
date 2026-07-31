# ADR 0001 — Use ChromaDB as the Semantic Memory Store

- **Date:** 2026-07-31
- **Status:** Accepted
- **Phase / milestone:** M2 – Memory Retrieval & Storage

## Context

The Conversational Memory Intelligence System requires a persistent vector database to store and retrieve user memories efficiently. The solution must support semantic similarity search, integrate well with Python, and be lightweight enough for local development.

## Decision

Use ChromaDB as the vector database for storing and retrieving semantic memories generated from user conversations.

## Consequences

### Positive

- Supports efficient semantic similarity search.
- Easy Python integration.
- Lightweight and suitable for local development.
- Works well with embedding models.

### Negative / Cost

- Not intended for very large distributed deployments.
- Requires embedding generation before storage.

### Invariant added to context-graph.json

Every stored memory must contain:
- User ID
- Embedding vector
- Metadata
- Original text

## Alternatives rejected

### FAISS

Rejected because it does not provide built-in metadata storage and persistence as conveniently as ChromaDB.

### PostgreSQL + pgvector

Rejected because it requires additional database administration and setup for this project.