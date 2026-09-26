# Implemented memory schema
Chroma stores ID (UUID), text document and normalized MiniLM embedding.
Metadata:
- user_id: immutable owner derived from authentication.
- memory_type: conversation | preference | fact | goal | task.
- importance, confidence: finite values in [0,1]; heuristic scores, not calibrated probabilities.
- created_at, updated_at: UTC ISO timestamps.
- expires_at: UTC timestamp; new records 1-7 days.
- source: manual | conversation | manual-correction | evaluation.
- conversation_id: bounded reference, not a transcript.
- version: incremented on explicit correction.
- deleted: retained for legacy compatibility; new DELETE physically removes the record.

Legacy missing expiry is tolerated without modifying existing data. Malformed expiry fails closed.
Owner is required on all ID-based reads, writes and deletes. Correcting a memory does not extend retention.
