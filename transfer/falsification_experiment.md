# Falsification Experiment

## Hypothesis
A hybrid educational-memory retriever will outperform semantic-only retrieval on relevance and stale-memory handling while maintaining zero cross-learner leakage.

## Setup
Create a held-out dataset containing correct recent evidence, stale evidence, misconceptions, unrelated semantically similar memories, conflicting evidence, low-confidence memories, and memories belonging to another learner.

Compare:
- **Baseline:** embedding similarity + learner isolation.
- **Proposal:** learner/subject/skill constraints + semantic candidates + evidence-aware ranking + recency/confidence/conflict handling.

## Metrics
1. Recall@k
2. Precision@k
3. Stale-memory rate
4. Unmarked-conflict rate
5. Cross-learner leakage rate
6. Human-rated pedagogical usefulness

## Falsification criterion
The proposal is falsified if it does not improve precision and stale-memory handling over the baseline while maintaining zero leakage. It is especially weakened if semantic-only retrieval performs equally well or better across most metrics.

## Controls
Use separate development and held-out test data. Do not tune the hybrid scoring function on the final test set.
