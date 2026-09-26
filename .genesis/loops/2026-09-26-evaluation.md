# Evaluation cycle — 2026-09-26
Scope: executable naive baseline, fixed JSONL, comparable metrics and reusable verification contract.
Changes: baseline.py, run_evaluation.py, contract and deliberate-fault tests.
Observed failure: semantic threshold missed a vague preference query. Added whole-term lexical candidate rescue.
Benchmark correction: replaced malformed long-context NaN fixture; archived earlier exploratory results as invalid for comparison.
Gate evidence: offline/semantic outputs and tests. Independent review pending.
