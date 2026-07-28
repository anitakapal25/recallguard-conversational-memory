Single stateless model call
→ loses information between requests
→ include recent conversation turns

Recent-turn context
→ older but important facts disappear
→ replay the entire conversation

Full conversation replay
→ exceeds token limits and increases cost and latency
→ summarize conversation history

Single rolling summary
→ loses detail, provenance, and corrections
→ retrieve selected past information

Similarity-only retrieval
→ returns irrelevant, stale, contradictory, or wrong-user information
→ managed conversational memory


| Stage | Approach                  | Assumption                                      | Observed bottleneck                                     | Pressure toward next approach                            |
| ----- | ------------------------- | ----------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| 1     | Stateless calls           | Every request contains all required information | No continuity between interactions                      | Carry prior turns forward                                |
| 2     | Recent-turn window        | Recent information is the most important        | Older preferences and decisions disappear               | Replay more history                                      |
| 3     | Full history replay       | More context always improves answers            | Token overflow, latency, cost, privacy exposure         | Compress the history                                     |
| 4     | Rolling summary           | One summary preserves all important information | Detail and provenance are lost; summaries become stale  | Retrieve selected evidence                               |
| 5     | Similarity-only retrieval | Semantic similarity equals usefulness           | Stale, contradictory, sensitive, and cross-user results | Add managed admission, ranking, lifecycle, and isolation |


Transformer

↓

Finite Context Window

↓

Older messages removed

↓

Information forgotten

↓

Need external retrieval

↓

Retrieval-Augmented Generation (RAG)

↓

Still no persistent user memory

↓

Conversational Memory Systems

↓

Managed Memory Intelligence
