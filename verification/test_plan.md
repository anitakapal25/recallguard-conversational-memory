# RecallGuard Conversational Memory System
# Verification Test Plan

## 1. Purpose

This test plan verifies that the RecallGuard conversational memory system
satisfies the functional, reliability, privacy, and lifecycle requirements
defined for the project.

The verification focuses on the complete memory lifecycle:

Conversation
→ Extraction
→ Admission
→ Storage
→ Retrieval
→ Ranking
→ Context Construction
→ LLM Response
→ Reflection
→ Deletion

The objective is not only to verify that individual components work, but
also that the complete pipeline behaves correctly under realistic
conversational scenarios.

---

## 2. System Under Test

The system consists of:

- Flask API
- Chat UI
- Rule-based memory extractor
- AdmissionEngine
- ChromaDB vector memory store
- Sentence Transformer embeddings
- MemoryRetriever
- MemoryRanker
- ContextBuilder
- ReflectionEngine
- Authentication and authorization
- PII filtering
- Local/free LLM
- Memory lifecycle and deletion
- Logging

Primary endpoints:

- `GET /health`
- `POST /chat`
- `POST /memory`
- `POST /retrieve`
- `POST /context`
- `POST /reflection`
- `GET /memories`
- `DELETE /memory/<memory_id>`

---

## 3. Verification Strategy

Verification is divided into:

1. Unit testing
2. Integration testing
3. End-to-end testing
4. Retrieval evaluation
5. Memory lifecycle testing
6. Security and privacy testing
7. Context-budget testing
8. LLM integration testing
9. Baseline comparison

Tests should be executed against the local development environment.

---

# 4. Functional Verification

## TEST-001: Health Check

### Objective
Verify that the Flask service is running correctly.

### Request

```http
GET /health