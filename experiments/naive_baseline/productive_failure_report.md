# Productive Failure Report

## Objective

Evaluate the naive conversational memory system and identify its limitations.

---

## Failure 1 - Outdated Memory

Scenario

User initially said:

"I live in Mumbai."

Later updated:

"I moved to Bangalore."

Question

"Where do I live?"

Expected

Bangalore

Observed

Mumbai

Reason

Similarity search does not understand that newer information should replace older information.

---

## Failure 2 - Contradictory Preferences

Scenario

"My favourite colour is Blue."

Later

"My favourite colour is Green."

Observed

Both memories were retrieved.

Reason

The system stores every message without resolving contradictions.

---

## Failure 3 - Irrelevant Retrieval

Scenario

User asks about programming.

Retrieved memories also included travel history.

Reason

Embedding similarity alone is insufficient for ranking.

---

## Failure Summary

Current limitations

- No recency awareness
- No importance scoring
- No contradiction handling
- No memory lifecycle
- No summarization
- No memory deletion