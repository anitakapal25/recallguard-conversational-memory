First principle 1: Context is finite

Observation:

The model cannot receive unlimited historical information.

Therefore:

historical information must be selected;
selection must respect a token budget;
less useful information must be pruned or compressed.

Derived capability:

Context budgeting and selection

First principle 2: Not every utterance deserves retention

Observation:

Conversations contain durable facts, temporary details, noise, secrets, and incorrect statements.

Therefore:

information must pass an admission decision;
memories need types and confidence;
sensitive content requires special handling.

Derived capability:

Memory extraction, classification, admission, and PII filtering

First principle 3: Relevance is not the same as similarity

Observation:

A semantically similar record may be stale, unimportant, invalid, or belong to another user.

Therefore ranking must consider:

relevance;
recency;
importance;
confidence;
validity;
ownership;
diversity.

Derived capability:

Multi-signal retrieval and ranking

First principle 4: User information changes

Observation:

Preferences, plans, roles, and circumstances evolve.

Therefore:

memories need timestamps and provenance;
newer information may supersede older information;
contradictions must be detected;
records may require consolidation or expiration.

Derived capability:

Lifecycle management and conflict resolution

First principle 5: Shared infrastructure creates isolation risk

Observation:

Similar language from different users may occupy the same retrieval system.

Therefore:

every record must be tenant-scoped;
authorization must be applied before or during retrieval;
cross-tenant leakage must be tested adversarially.

Derived capability:

Tenant-aware storage, authorization, and isolation