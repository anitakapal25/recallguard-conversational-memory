# PLAN — recallguard-conversational-memory

The machine-parseable implementation plan. Mirrors the milestone table in `DONE.html` (DONE.html is the
human/visual view; this is the one loops read). Sliced so each milestone ships in one L1 BUILD pass.

> Slicing rule: a milestone must have (a) a single clear outcome, (b) an exact **demo command** that
> proves it, and (c) a freeze boundary of files it may touch. If you can't write the demo command,
> the milestone is too vague — split it.

---

## Brainstorm (G0.5 — fill before slicing milestones)

> Three fundamentally different approaches to the cognitive job. Pick one. Record the rationale.
> This is the cheapest design decision — you haven't written a line of code yet.

### Approach A — Retrieval-Augmented Memory (RAG)
Use vector embeddings stored in ChromaDB to retrieve relevant memories and inject them into the prompt before generating responses.
- Strengths: • Simple architecture
              • Fast semantic retrieval
              • Easy to scale
              • Low latency
- Weaknesses: • Depends on embedding quality
• Limited reasoning over long-term memory

### Approach B — Full Conversation History
Store the complete conversation history and send it to the LLM for every request.
- Strengths: • Simple implementation
• No retrieval logic required
- Weaknesses: • High token usage
• Doesn't scale
• Expensive

### Approach C — Hybrid Memory System
Combine semantic memory retrieval with conversation history and summarization.
- Strengths: • Best contextual understanding
• Supports long conversations
- Weaknesses: • More complex implementation
• Higher maintenance cost

### Chosen: Hybrid Memory System — Provides scalable semantic retrieval while maintaining conversational context and minimizing token usage.

---

## Milestones

### M1 — Memory Extraction & Storage
- **Outcome:** Extract user memories from conversations and store vector embeddings in ChromaDB.

- **Phase (swe-master):** Build
- **Files / freeze boundary:** 
implementation/memory.py
implementation/database.py
- **Demo command:** python implementation/app.py

- **Success criteria:** User memories are extracted, embedded, and successfully stored in ChromaDB.

- **Loops:** L1, L4
- **Skills:** canon + tdd + data-systems-engineering
- **Token budget:** 50000

### M2 — Memory Retrieval

- **Outcome:**
Retrieve relevant memories using semantic similarity search.

- **Phase:**
Build

- **Files:**
implementation/database.py
implementation/memory.py

- **Demo command:**
python implementation/app.py

- **Success criteria:**
Relevant memories are returned for a user query.

- **Loops:**
L1, L3, L4

- **Skills:**
canon + tdd + vector-search

- **Token budget:**
50000

### M3 — Prompt Construction

- **Outcome:**
Construct prompts using retrieved memories.

- **Phase:**
Build

- **Files:**
implementation/prompt.py

- **Demo command:**
python implementation/app.py

- **Success criteria:**
Retrieved memories are injected into prompts before LLM inference.

- **Loops:**
L1, L4

- **Skills:**
canon + tdd + prompt-engineering

- **Token budget:**
50000

### M4 — LLM Response Generation

- **Outcome:**
Generate grounded responses using retrieved context.

- **Phase:**
Build

- **Files:**
implementation/llm.py

- **Demo command:**
python implementation/app.py

- **Success criteria:**
LLM produces responses that use retrieved memories correctly.

- **Loops:**
L1, L4

- **Skills:**
canon + llmops-ai-agents

- **Token budget:**
50000

### M5 — FastAPI Integration

- **Outcome:**
Expose the conversational memory system through a REST API.

- **Phase:**
Integration

- **Files:**
implementation/app.py

- **Demo command:**
python implementation/app.py

- **Success criteria:**
API accepts requests and returns context-aware responses.

- **Loops:**
L1, L4

- **Skills:**
canon + production-readiness

- **Token budget:**
50000

### M6 — Verification & Documentation

- **Outcome:**
Complete verification, documentation, and project artifacts.

- **Phase:**
Verify

- **Files:**
verification/
.genesis/

- **Demo command:**
python implementation/app.py

- **Success criteria:**
All deliverables are complete and documentation reflects the implemented system.

- **Loops:**
L1, L4

- **Skills:**
canon + qa

- **Token budget:**
50000

---

## Progress

- Deliverable 1 completed: Research and project setup.
- Deliverable 2 completed: System architecture and design.
- Deliverable 3 completed: Implementation of conversational memory pipeline.
- Deliverable 4 completed: Initial evaluation and verification.
