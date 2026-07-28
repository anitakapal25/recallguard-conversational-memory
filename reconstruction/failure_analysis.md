## Evolution of Conversational Memory

Approach 1: Stateless model calls

Failure case 1: Stateless assistant
Assumption

Every user request contains all information required to answer it.

Scenario

Conversation 1:

User: I am vegetarian and allergic to peanuts.

Conversation 2, several days later:

User: Suggest a high-protein lunch.

Failure

The assistant suggests a chicken dish or a peanut-based meal because the earlier constraint is absent from the current input.

Impact
unsafe or unsuitable answer;
repeated user effort;
loss of trust.
Requirement derived

The system must preserve selected durable user information across sessions.

Failure case 2: Full conversation replay
Assumption

Providing the complete history is always the most accurate approach.

Scenario

A user has a six-month interaction history containing hundreds of messages.

Failure
context exceeds the model’s input limit;
prompt cost grows continuously;
response latency increases;
irrelevant personal information is repeatedly exposed to the model;
useful information may be buried among unrelated messages.
Requirement derived

The system must select a bounded subset of prior information rather than replay everything.

Failure case 3: Rolling summary
Assumption

A single continuously updated summary can represent the whole conversation.

Scenario

The summary says:

User prefers morning meetings.

Later, the user says:

My schedule changed. Please arrange meetings after 3 p.m.

Failure

The summary may preserve the earlier preference, merge both statements ambiguously, or lose when and why the change occurred.

Impact

The assistant acts on stale information.

Requirement derived

The system needs timestamps, provenance, update handling, supersession, and conflict resolution.

Failure case 4: Similarity-only retrieval
Assumption

The most semantically similar item is the most useful item.

Scenario

Stored memories:

“User prefers Python for data work.”
“User previously preferred Java.”
“Another user prefers Python.”
“User mentioned Python while discussing a temporary bug.”

Query:

Which language should I use for this data-analysis project?

Failure

Similarity alone may return:

the outdated Java preference;
another user’s Python preference;
a temporary technical mention rather than a durable preference.
Requirement derived

Retrieval must use multiple signals, including:

relevance;
recency;
importance;
confidence;
tenant identifier;
memory type;
temporal validity.
Failure case 5: Store everything
Assumption

More stored information produces better future responses.

Scenario

The user shares:

My temporary verification code is 284019.

Failure

The value is retained and may later appear in retrieval results, logs, backups, or debugging traces.

Requirement derived

The system needs an admission policy, sensitive-data detection, retention rules, auditability, and deletion support.


| Claim                                              | Current support                                   | Later validation                                             |
| -------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------ |
| Full replay increases token use                    | Direct consequence of growing prompt length       | Measure tokens across histories of different sizes           |
| Similarity-only retrieval may return stale facts   | Constructed failure case and retrieval literature | Build fixed contradictory-memory dataset                     |
| Cross-user retrieval is a serious boundary failure | Security requirement                              | Adversarial tenant-isolation test                            |
| Rolling summaries may lose provenance              | Reasoned limitation                               | Compare source recovery from summaries vs structured records |
