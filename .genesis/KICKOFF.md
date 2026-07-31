# KICKOFF — Conversational Memory Intelligence System (RecallGuard)

> Works in any agent. Replace the skill-invocation syntax per `AGENT-ADAPTERS.md`
> (Hermes `skill_view(name=…)` · Claude Code `Skill`/`/x` · Codex `$x`). The rest is identical.

```
Load skills (skill canon — always):

- agentic-swe-master
- coding-orchestrator
- modular-architecture
- production-readiness
- llmops-ai-agents
- data-systems-engineering
- prompt-engineering

Read in order:
- AGENTS.md / CLAUDE.md                       (repo governance)
- .genesis/DONE.html                          (locked spec + definition of done + plan)
- .genesis/PLAN.md                            (milestones being executed)
- .genesis/wiki/index.md                      (then drill into pages matching the milestone's nouns)
- .genesis/implementation-notes.html          (search for the milestone's nouns — what's LIVE now)
- .genesis/LOOPS.md                           (how the work gets done)
- .genesis/checkpoints/CURRENT.md             (where we are, if it exists)

Then:
1. Pick the next milestone from PLAN.md:

M1 – Memory Extraction & Storage
M2 – Memory Retrieval
M3 – Prompt Construction
M4 – LLM Response Generation
M5 – FastAPI Integration
M6 – Verification & Documentation

2. Start the application:

   python -m uvicorn implementation.app:app --reload

3. Execute the milestone.

4. Verify:

   - POST /chat
   - Memory stored in ChromaDB
   - Memory retrieved
   - Prompt includes retrieved memories
   - AI response is context-aware

5. Update CURRENT.md and implementation-notes.html.

6. Complete L4 VERIFY before marking the milestone done.

Stop rules: if any gate fails 3 times, stop, write what you tried to CURRENT.md, surface to the user.
Never mark a milestone done without L4 VERIFY APPROVE. Never edit DONE.html / PLAN.md without being asked.
```
