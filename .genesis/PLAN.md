# PLAN — recallguard-conversational-memory

The machine-parseable implementation plan. Mirrors the milestone table in `DONE.html` (DONE.html is the
human/visual view; this is the one loops read). Sliced so each milestone ships in one L1 BUILD pass.

> Slicing rule: a milestone must have (a) a single clear outcome, (b) an exact **demo command** that
> proves it, and (c) a freeze boundary of files it may touch. If you can't write the demo command,
> the milestone is too vague — split it.

---

# Brainstorm (G0.5 — fill before slicing milestones)

> Three fundamentally different approaches to the cognitive job. Pick one. Record the rationale.
> This is the cheapest design decision — you haven't written a line of code yet.

## Approach A — Stateless RAG

A traditional Retrieval-Augmented Generation pipeline that retrieves relevant documents for every user query without maintaining long-term conversational memory.

- Strengths:
  - Simple architecture
  - Fast implementation
  - Easy to scale

- Weaknesses:
  - No persistent memory
  - Poor long-term personalization
  - Repeats previously known information


## Approach B — Hierarchical Conversational Memory + RAG ✅

Augment RAG with a memory management layer consisting of Working Memory, Episodic Memory, Semantic Memory, and Long-term Memory. Retrieved memories become part of the prompt context.

- Strengths:
  - Long-term personalized conversations
  - Smaller context windows
  - Better factual consistency
  - Memory consolidation and forgetting

- Weaknesses:
  - Higher architectural complexity
  - Requires memory ranking and lifecycle management


## Approach C — MemGPT-style Virtual Context Manager

Implement a MemGPT-inspired architecture that continuously swaps memories between working context and external storage.

- Strengths:
  - Extremely scalable conversations
  - Efficient context usage

- Weaknesses:
  - More complex orchestration
  - Harder debugging
  - Higher latency


## Chosen: Approach B

Hierarchical Conversational Memory + RAG

### Rationale

The objective of RecallGuard is to improve conversational AI by introducing persistent, trustworthy memory rather than simply retrieving documents. A layered memory architecture aligns best with the project's goals while remaining practical to implement and evaluate.

---

# Milestones

## M1 — Project Foundation

**Outcome**

Create the complete project skeleton including backend, Docker environment, PostgreSQL, Vector Database integration, CI pipeline, and coding standards.

**Phase (swe-master)**

Foundation

**Files / freeze boundary**

```
backend/**
docker/**
docker-compose.yml
requirements.txt
README.md
```

**Demo command**

```bash
docker compose up
```

**Success criteria**

- Backend starts successfully
- PostgreSQL container running
- Vector database running
- Health endpoint responds successfully

**Loops**

L1 BUILD → L4 VERIFY

**Skills**

canon + tdd + modular-architecture + production-readiness

**Token budget**

50000

---

## M2 — Memory Ingestion Pipeline

**Outcome**

Extract memories from conversations and persist them in PostgreSQL and the vector database.

**Phase**

Implementation

**Files**

```
backend/memory/**
backend/services/**
backend/models/**
```

**Demo command**

```bash
python demo/store_memory.py
```

**Success criteria**

- Memory extracted
- Embeddings generated
- Memory persisted successfully

**Loops**

L1 BUILD → L3 RESEARCH → L4 VERIFY

**Skills**

canon + llmops + data-systems-engineering

**Token budget**

50000

---

## M3 — Semantic Memory Retrieval

**Outcome**

Retrieve the most relevant memories using vector similarity and ranking.

**Phase**

Implementation

**Files**

```
backend/retrieval/**
backend/vectorstore/**
```

**Demo command**

```bash
python demo/retrieve_memory.py
```

**Success criteria**

- Top-K memories returned
- Ranking works correctly
- Retrieval latency acceptable

**Loops**

L1 BUILD → L2 DEBUG → L4 VERIFY

**Skills**

canon + retrieval-engineering + tdd

**Token budget**

50000

---

## M4 — Context Builder & RAG

**Outcome**

Construct prompts by combining user input, retrieved memories, and external knowledge before sending them to the LLM.

**Phase**

Implementation

**Files**

```
backend/rag/**
backend/prompts/**
```

**Demo command**

```bash
python demo/chat.py
```

**Success criteria**

- Context assembled correctly
- Memory injected into prompts
- LLM responses use retrieved memories

**Loops**

L1 BUILD → L4 VERIFY

**Skills**

canon + llmops + prompt-engineering

**Token budget**

50000

---

## M5 — Memory Lifecycle Management

**Outcome**

Implement consolidation, summarization, decay, and forgetting of memories.

**Phase**

Optimization

**Files**

```
backend/memory/**
backend/lifecycle/**
```

**Demo command**

```bash
python demo/consolidate_memory.py
```

**Success criteria**

- Duplicate memories merged
- Old memories summarized
- Forgetting policy enforced

**Loops**

L1 BUILD → L3 RESEARCH → L4 VERIFY

**Skills**

canon + data-engineering + tdd

**Token budget**

50000

---

## M6 — Evaluation & Deployment

**Outcome**

Evaluate memory quality and deploy the complete RecallGuard system.

**Phase**

Verification

**Files**

```
tests/**
evaluation/**
docker/**
```

**Demo command**

```bash
pytest && docker compose up
```

**Success criteria**

- All tests pass
- Evaluation metrics generated
- Deployment successful
- L4 VERIFY approves

**Loops**

L1 BUILD → L4 VERIFY

**Skills**

canon + production-readiness + qa

**Token budget**

50000

---

# Progress (loops append here on milestone completion — newest last)

- _(none yet — first BUILD loop will append milestone completion history.)_