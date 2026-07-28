# Component Scan

## Memory Representation

Paper
Memory Networks

Idea

Store memories separately from the LLM.

Benefit

Large memory without increasing prompt size.

Applicability

Useful.

---

## Retrieval

Paper

RAG

Idea

Retrieve only relevant memories.

Current Problem

Entire conversation cannot fit inside context window.

Decision

Useful.

---

## Ranking

Paper

Generative Agents

Idea

Ranking should use

- relevance
- recency
- importance

Current System

Uses only similarity.

Decision

Prototype later.