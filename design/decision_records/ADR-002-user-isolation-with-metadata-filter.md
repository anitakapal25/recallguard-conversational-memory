# ADR-002: User Isolation with Metadata Filtering

## Status

Accepted

## Date

2026-08-07

## Context

The system stores memories belonging to different users.

A retrieval request must never return memories belonging to another user. User isolation therefore needs to be enforced at the persistence/retrieval boundary rather than relying only on application-level filtering.

## Decision

Use the `user_id` metadata field in ChromaDB and apply it as a mandatory filter during memory retrieval and listing.

The retrieval query combines:

* `user_id == requested user`
* `deleted == False`

## Rationale

Filtering directly in the ChromaDB query reduces the amount of unrelated data returned to the application and creates a stronger isolation boundary.

For example, retrieval follows the conceptual rule:

```text
user_id = requested_user
AND
deleted = false
```

This also allows the same ChromaDB collection to contain memories for multiple users.

## Alternatives Considered

### Separate collection per user

Rejected because it would create unnecessary collection-management overhead as the number of users grows.

### Retrieve everything and filter in Python

Rejected because unrelated memories would already have crossed the persistence boundary into application memory.

### Separate database per user

Rejected because it introduces unnecessary operational complexity for the current project.

## Trade-offs

### Advantages

* Simple implementation
* Efficient metadata filtering
* Supports multiple users in one collection
* Reduces accidental cross-user retrieval
* Easy to test

### Disadvantages

* Correct filtering must be consistently applied to every relevant query
* Metadata integrity becomes important
* Production systems would require additional authorization and tenant-boundary controls

## Consequences

MemoryStore is responsible for applying user-level filters to retrieval and listing operations.

The retrieval test suite includes a user-isolation test to verify that one user's memories are not returned for another user.

## Review Trigger

Revisit this design when introducing multi-tenant production infrastructure, more complex authorization rules, or additional tenant-level access policies.
