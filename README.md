# RecallGuard - Conversational Memory Intelligence System

## Overview

RecallGuard is a conversational memory system that stores, retrieves, ranks, and manages long-term memories for AI assistants using ChromaDB and Sentence Transformers.

## Features

- Persistent memory storage using ChromaDB
- Semantic search with embeddings
- Memory ranking
- Context building
- Reflection engine
- Duplicate detection
- Soft deletion
- Confidence filtering
- User isolation
- Structured logging
- Basic authentication
- REST API
- Unit testing with pytest

---

## Project Structure

```
implementation/
│
├── app.py
├── auth.py
├── config.py
├── context_builder.py
├── database.py
├── logger.py
├── memory_store.py
├── models.py
├── ranking.py
├── reflection.py
├── retrieval.py
├── test_memory_store.py
└── test_retrieval.py
```

---

## Installation

```bash
git clone <repository>
cd recallguard-conversational-memory

pip install -r requirements.txt
```

---

## Run

```bash
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

## Run Tests

```bash
pytest -v
```

---

## Technologies Used

- Python
- ChromaDB
- Sentence Transformers
- Flask
- PyTest

---

## Deliverable 6 Components

- Persistent Memory Store
- Retrieval Engine
- Ranking Module
- Context Builder
- Reflection Module
- Logger
- Authentication
- REST API
- Unit Tests

---

## Future Enhancements

- Redis caching
- JWT authentication
- Role-based access control
- Memory summarization
- Multi-agent memory sharing
- Dashboard and analytics