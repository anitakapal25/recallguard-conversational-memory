# ADR-004: Collection Abstraction Through MemoryStore

## Status

Accepted

## Date

2026-08-08

## Context

Several components of RecallGuard need access to stored memories.

Directly exposing the ChromaDB collection to every component would tightly couple the entire application to the database implementation.

During development, this coupling also made testing more difficult because tests could unintentionally reuse persistent collections and data from previous executions.

## Decision

Introduce `MemoryStore` as the primary abstraction around the ChromaDB collection.

`MemoryStore` obtains a collection through the database layer:

```text
Application
    ↓
MemoryStore
    ↓
database.get_collection()
    ↓
ChromaDB
```

Tests can create a dedicated collection through:

```text
MemoryStore(collection_name="test_<unique_id>")
```

## Rationale

The abstraction provides a single boundary for memory persistence operations.

Responsibilities include:

* Adding memories
* Retrieving memories
* Listing memories
* Updating memories
* Soft deletion
* Duplicate detection
* Expiration
* Memory-type queries

This keeps ChromaDB-specific operations out of retrieval, reflection, and API code.

## Alternatives Considered

### Direct ChromaDB access from every module

Rejected because it creates tight coupling and duplicated database logic.

### Global collection variable

Rejected because it makes testing and multiple collection instances difficult.

### Full repository framework

Rejected because it would introduce unnecessary abstraction and complexity for the current project.

## Trade-offs

### Advantages

* Clear separation of concerns
* Easier unit testing
* Easier database replacement in the future
* Supports isolated test collections
* Centralizes persistence behavior

### Disadvantages

* Adds an abstraction layer
* Requires careful maintenance of the MemoryStore interface
* Some ChromaDB-specific capabilities may need explicit wrapper methods

## Consequences

Application components depend on `MemoryStore` rather than directly accessing ChromaDB.

The test suite can create unique collections for each test fixture, preventing persistent data from previous test runs from affecting retrieval results.

This design directly helped resolve failures involving confidence filtering and user isolation.

## Review Trigger

Reconsider the abstraction if the persistence layer becomes significantly more complex or if the system migrates to another vector database.
