# Reproducible baseline protocol
Date: 2026-09-26. Dataset: verification/evaluation_dataset.jsonl (16 development scenarios; hash recorded per run).
Run: python verification/run_evaluation.py [--semantic].
Both pipelines use identical messages, queries, ownership and encoder. Baseline uses raw append-only storage and similarity-only top-k with owner filtering. Corrections append new statements; lifecycle requests are unsupported, not secretly applied.
Improved pipeline applies privacy/admission, explicit corrections, expiry, deletion, relevance threshold, multi-signal ranking and bounded context.
Do not interpret baseline lifecycle failure as a retrieval-algorithm advantage: results compare complete policies.

7 retrieval calls per scenario; report first call and nearest-rank p50/p95 including that first call.
Measure precision/recall at requested k, exact case pass, stored record count, stored UTF-8 content bytes and rendered prompt UTF-8 units.
Empty expected/result sets score 1; false positives in empty-expected cases score 0.
Byte units are not measured model tokens; content bytes are not on-disk index size.
No response-quality claim is made by this offline runner. Live smoke checks one separate synthetic response scenario.
Dataset is a development/regression workload, not held out. Do not claim generalization from it.
Results: verification/results/offline and verification/results/semantic. Preserve failures in error_examples.jsonl.
