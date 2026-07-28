# Problem Reconstruction

## 1. Problem Statement

Conversational AI systems process each interaction using only information included in current context window. When conversation grow longer important information may be compressed or lost.
Because of this an assistant may ask for information the use has already provided, apply outdated preferences, or mix information beloging to other users.

## 2. Affected Users

### End users

Users expect the assistant to remember stable preferences, ongoing tasks,
corrections, and relevant history.

### Application developers

Developers need predictable memory behaviour rather than unexplained retrieval
or hidden model state.

### System operators

Operators need to monitor latency, storage growth, retrieval failures, privacy
events, and deletion behaviour.

### Security and compliance teams

These teams need guarantees that sensitive information is handled correctly,
deleted when required, and never exposed to another user.

There are consequences such as

repetitive conversations
inconsistent personalisation
outdated recommendations
incorrect answers
cross-user leakage
excessive prompt cost

## Constraints
| Constraint           | Why it matters                                     | Example failure                              |
| -------------------- | -------------------------------------------------- | -------------------------------------------- |
| Token budget         | Full history cannot always fit in the prompt       | Important older details are removed          |
| Latency              | Retrieval and ranking add processing time          | The assistant responds too slowly            |
| Cost                 | Larger prompts and storage increase operating cost | Every request sends unnecessary history      |
| Privacy              | Conversations may contain sensitive information    | Private data is stored without justification |
| Correctness          | Memories may become outdated or contradictory      | An old preference overrides a new one        |
| Multi-user isolation | Each user’s information must remain separate       | One user receives another user’s memory      |


Success criteria

Include criteria such as:

useful prior information is available when needed;
irrelevant information is excluded;
current preferences outrank outdated ones;
sensitive information is not retained without policy justification;
no cross-user information is retrieved;
context remains within the token budget;
deletion affects both primary storage and retrieval paths;
decisions are traceable through logs.