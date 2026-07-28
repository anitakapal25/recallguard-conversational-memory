# Challenge Notes

Question

Why not use only similarity search?

Answer

Similarity ignores

- recency
- importance
- conflicting memories

Decision

Need ranking.

---

Question

Why use vector database?

Answer

Conversation history becomes very large.

Decision

Use ChromaDB.

---

Question

Can retrieval return wrong memories?

Answer

Yes.

Need reranking.