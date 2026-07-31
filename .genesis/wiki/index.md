# Wiki Index — recallguard-conversational-memory

The project knowledge base. Same schema as the agentic-swe-kit wiki: concept pages in `concepts/`,
each with frontmatter and ≥2 `[[wikilinks]]`. The L3 RESEARCH loop writes here; G0 reads here first.

> **Read this file before any milestone (G0 step 1).** Pick candidate pages by name-matching the
> milestone's nouns, then drill in. The wiki is what prevents rebuilding work that already exists.

---

# Entities (the things this system has)

- [[FastAPI]] — REST API exposing the conversational memory service.
- [[ChromaDB]] — Vector database for storing semantic memories.
- [[OpenAI Embeddings]] — Converts memories into vector embeddings.
- [[Memory Store]] — Persistent storage of user memories.
- [[LLM]] — Generates context-aware responses.
- [[Prompt Builder]] — Injects retrieved memories into prompts.
- [[User]] — Source of conversational input.
- [[Conversation]] — Sequence of user and assistant messages.

---

# Concepts (how it works)

- [[Semantic Memory]] — Stores meaningful user information using embeddings.
- [[Memory Extraction]] — Identifies important facts from conversations.
- [[Memory Retrieval]] — Finds relevant memories through similarity search.
- [[Prompt Engineering]] — Builds prompts enriched with retrieved memories.
- [[Retrieval-Augmented Generation (RAG)]] — Uses retrieved memories to improve LLM responses.
- [[Context Injection]] — Adds retrieved memories into the prompt.
- [[Verification]] — Confirms that responses satisfy project requirements.

---

# Sources (research distilled by L3)

- [[RAG]] — Retrieval-Augmented Generation architecture.
- [[MemGPT]] — Memory management for LLM agents.
- [[Generative Agents]] — Long-term memory for autonomous agents.
- [[FAISS and HNSW]] — Vector similarity search algorithms.
- [[Microsoft Open-weight Models]] — Research on open-weight AI models.

---

# Seeded from agentic-swe-kit

Relevant concept areas used in this project:

- Clean Architecture
- Modular Architecture
- LLMOps
- Data Systems Engineering
- Prompt Engineering
- Production Readiness
- Security Engineering
- Verification