# ADR-006: Lexical rescue for semantic candidate admission
Date: 2026-09-26
Status: accepted for the local development suite

Observation: a vague preference query failed the 0.4 embedding threshold despite matching the stored verb. Similarity alone can also underweight rare terms in long text.
Decision: accept a semantic candidate if similarity >=0.4 OR every non-stopword query term appears as a whole word in the document.
All ownership, expiration, confidence and type filters remain mandatory. The original similarity is retained for ranking; the result exposes lexical_match.
Limits: this is candidate rescue inside the top-100 semantic pool, not exhaustive hybrid indexing or semantic contradiction resolution.

Evidence correction: during investigation, the long-context fixture was discovered to contain JavaScript-generated NaN strings instead of long text. Corrected JSONL hash is recorded in new results; a fixture-length regression test prevents recurrence.
pre-hybrid results use the invalid earlier fixture and MUST NOT be used as a like-for-like performance claim.
Both corrected baseline and improved benchmarks are rerun. The dataset is development data; no held-out performance claim.
