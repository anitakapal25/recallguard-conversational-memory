# Current API contracts
See README for endpoint list, authentication and error semantics.
All object operations derive owner identity from X-API-Key and apply it in storage queries.
Client user_id values never authorize another owner.

POST /memory: JSON object with text (1-4000 characters), consent=true, optional known memory_type, finite importance/confidence in [0,1], retention_days integer 1-7.
Returns 201 {status:stored,memory_id} or 200 {status:duplicate,memory_id}.

PUT /memory/{id}: text and consent=true. Explicitly replaces owned active content/vector, increments version, preserves expires_at. Returns 404 for absent/foreign/expired records.
DELETE /memory/{id}: removes owned content/vector, including expired records. Returns 404 for absent/foreign records.
GET /memories: active records in Chroma columnar shape {ids,documents,metadatas}.
POST /retrieve: query and optional integer top_k (1-20). Returns ranked {id,content,similarity,metadata} rows.
POST /context: query. Returns prompt and conservative budget statistics.
POST /chat: message, optional boolean remember=false and conversation_id (<=128 characters). Returns generation_status, response, stored_memories, retrieved memories, stats, request_id.
503 generation failure can follow a successful write; stored_memories is authoritative for that request.

64 KiB request-body limit. JSON objects only. Invalid values return 400.
Internal errors return generic 503 with request ID, not exception details.
