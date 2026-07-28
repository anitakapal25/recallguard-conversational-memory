# KICKOFF — RecallGuard Conversational Memory Intelligence System

Project
-------
RecallGuard is an AI-native conversational memory intelligence system that augments Retrieval-Augmented Generation (RAG) with hierarchical memory management. The goal is to provide persistent, context-aware conversations through working memory, episodic memory, semantic memory, and long-term memory.

Primary Architecture
--------------------
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Vector Store: pgvector
- Cache: Redis
- LLM: OpenAI GPT
- Embeddings: OpenAI text-embedding-3-large
- Containerization: Docker
- Architecture: Hexagonal Architecture + Domain-Driven Design

Load skills (always)
--------------------
- agentic-swe-master
- coding-orchestrator
- modular-architecture
- production-readiness
- data-systems-engineering
- llmops-ai-agents
- security-engineering
- tdd

Read in order
-------------
1. AGENTS.md / CLAUDE.md
2. .genesis/DONE.html
3. .genesis/PLAN.md
4. .genesis/wiki/index.md
5. .genesis/implementation-notes.html
6. .genesis/LOOPS.md
7. .genesis/checkpoints/CURRENT.md (if present)

Execution Rules
---------------
1. Resume from CURRENT.md if it exists.
2. Otherwise pick the next unfinished milestone from PLAN.md.
3. Run G0 Existence Pre-Flight before building.
4. Execute the milestone using the L1 BUILD loop.
5. Enforce all Genesis gates (G1–G5).
6. Use L2 DEBUG and L3 RESEARCH only when required.
7. Finish every milestone with an independent L4 VERIFY session.
8. Update CURRENT.md, implementation-notes.html, and PLAN.md after successful verification.

Project Goals
-------------
M1 – Project Foundation
M2 – Memory Ingestion Pipeline
M3 – Semantic Retrieval
M4 – Context Builder & RAG
M5 – Memory Lifecycle Management
M6 – Evaluation & Deployment

Definition of Success
---------------------
- Persistent conversational memory
- Accurate semantic retrieval
- Memory-aware prompt construction
- Successful end-to-end chat
- All tests passing
- Docker deployment working
- L4 VERIFY approval