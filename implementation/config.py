"""
config.py

Central configuration for the Conversational Memory System.
"""

from pathlib import Path

# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent

CHROMA_DB_PATH = BASE_DIR / "../chromadb"

# ==========================
# Collection
# ==========================

COLLECTION_NAME = "conversation_memory"

# ==========================
# Embedding Model
# ==========================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================
# Retrieval
# ==========================

TOP_K = 10

# ==========================
# Context Builder
# ==========================

MAX_CONTEXT_TOKENS = 1000

# ==========================
# Memory
# ==========================

DEFAULT_IMPORTANCE = 0.5

DEFAULT_CONFIDENCE = 0.9
# Duplicate Detection
DUPLICATE_SIMILARITY_THRESHOLD = 0.95