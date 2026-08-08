# ADR-001: ChromaDB as Vector Store

## Status

Accepted

## Date

2026-08-06

## Context

RecallGuard requires persistent storage for conversational memories and semantic retrieval of memories based on embeddings.

The system needs to support:

* Persistent vector storage
* Similarity search using embeddings
* Metadata filtering
* Multiple users
* Soft deletion
* Memory-type filtering
* Local development and testing without requiring a separate database service

Possible approaches included PostgreSQL with pgvector, FAISS, and ChromaDB.

## Decision

Use **ChromaDB** as the vector database for the conversational memory system.

ChromaDB is accessed through a dedicated database layer and `MemoryStore`, rather than directly from higher-level application components.

## Rationale

ChromaDB was selected because it provides:

1. Persistent vector storage
2. Native similarity search
3. Metadata filtering
4. Simple local deployment
5. Minimal infrastructure requirements
6. Straightforward Python integration

This makes it appropriate for the project's current development and evaluation stage.

## Trade-offs

### Advantages

* Easy to set up locally
* Persistent storage
* Supports embeddings and metadata together
* Good fit for semantic memory retrieval
* No separate database server required

### Disadvantages

* Not necessarily the final choice for a large production deployment
* Advanced operational requirements may eventually require a more scalable vector/database infrastructure
* Performance characteristics need further evaluation with production-scale data

## Consequences

The project stores each memory together with:

* Memory ID
* User ID
* Memory text
* Embedding
* Memory type
* Importance
* Confidence
* Creation timestamp
* Deleted state

Higher-level components do not need to know ChromaDB's implementation details.

## Review Trigger

Reconsider this decision if memory volume, concurrent traffic, availability requirements, or operational requirements exceed the capabilities appropriate for the current architecture.
