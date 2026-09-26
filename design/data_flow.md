# RecallGuard data flow
Revision: 2026-09-26.

## 1. Explicit memory write
API key -> authenticated owner -> consent=true -> input validation -> sensitive-pattern rejection -> exact duplicate lookup -> normalized embedding -> Chroma document/vector/metadata -> stored or duplicate response.

## 2. Chat
API key -> owner -> validate message and provenance reference -> sensitive-pattern rejection -> reject oversized base prompt -> optional extraction/admission if remember=true -> store decisions -> scoped retrieval/ranking -> bounded prompt -> Ollama -> response plus committed decisions and budget stats.
An inference error returns generation_status=unavailable and preserves visibility of any preceding successful writes.

## 3. Retrieval
Authenticated owner -> query validation -> active owned IDs -> semantic candidates -> hybrid candidate admission -> ranking -> top-k. Expired and deleted rows never qualify.

## 4. Explicit correction
Authenticated owner -> owned active ID lookup -> validate new text/privacy -> replacement embedding -> update content/vector/source/version; retain original ID, creation time and expiry. Old content is not retained as a hidden version.

## 5. Delete / expiry
Owned DELETE -> Chroma delete -> subsequent ID lookup and retrieval cannot find the record.
Read-time expiry -> record hidden immediately.
Scheduled sweep -> physical expired-record deletion -> content-free counts.

## 6. Evaluation
Fixed synthetic JSONL -> isolated baseline and improved collections -> same encoder/query workload -> seven retrieval timings per case -> CSV, summary hash and error examples. Live generation is a separate labeled smoke check.
