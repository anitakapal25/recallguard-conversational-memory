# ADR-003: Retrieval Similarity and Filtering Strategy

## Status

Accepted

## Date

2026-08-07

## Context

Semantic retrieval returns memories according to embedding similarity. However, similarity alone is not sufficient to determine whether a memory should be included in the final result.

The system also needs to consider:

* Memory type
* Confidence
* Deleted state
* User identity
* Top-k limits

An important distinction emerged during testing: the system's duplicate-detection threshold and retrieval filtering threshold serve different purposes.

## Decision

Use ChromaDB similarity search to obtain candidate memories and apply application-level filtering in `MemoryRetriever`.

The retrieval pipeline is:

```text
Query
  ↓
Generate embedding
  ↓
ChromaDB similarity search
  ↓
User/deleted filtering
  ↓
Confidence filtering
  ↓
Memory-type filtering
  ↓
Similarity ordering
  ↓
Top-K results
```

The duplicate-detection threshold remains separate from normal retrieval.

## Rationale

A single global similarity threshold would make the retrieval behavior unnecessarily rigid.

Different use cases have different requirements. For example, a memory may be useful even when it is not extremely similar to the query, while duplicate detection requires a much stricter similarity requirement.

The system therefore treats:

* similarity as the retrieval signal
* confidence as a memory-quality filter
* memory type as a semantic category filter
* duplicate similarity as a separate admission/maintenance rule

## Alternatives Considered

### One fixed similarity threshold

Rejected because a single threshold does not work equally well for retrieval and duplicate detection.

### Application-only vector search

Rejected because ChromaDB already provides efficient vector similarity search.

### Return ChromaDB results without filtering

Rejected because deleted, low-confidence, or incorrect memory types could reach downstream context construction.

## Trade-offs

### Advantages

* Flexible retrieval policy
* Clear separation of concerns
* Easy to test individual filtering rules
* Supports different memory types
* Allows future ranking improvements

### Disadvantages

* Retrieval behavior is split across storage and application layers
* Thresholds may require empirical tuning
* Embedding model quality affects retrieval quality

## Consequences

`MemoryRetriever` converts the query into an embedding, requests candidate memories from `MemoryStore`, filters the results, calculates similarity from the returned distance, and returns the final ordered list.

The test suite validates confidence filtering, memory-type filtering, top-k behavior, and similarity ordering.
