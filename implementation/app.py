"""
app.py

Main Flask application for the
Conversational Memory Intelligence System.
"""

from sentence_transformers import SentenceTransformer
from flask import Flask, jsonify, request

from auth import login_required
from config import EMBEDDING_MODEL
from context_builder import ContextBuilder
from logger import MemoryLogger
from memory_store import MemoryStore
from ranking import MemoryRanker
from reflection import ReflectionEngine
from retrieval import MemoryRetriever

app = Flask(__name__)

# --------------------------------------------------
# Components
# --------------------------------------------------

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

memory_store = MemoryStore()

retriever = MemoryRetriever(
    memory_store
)

ranker = MemoryRanker()

builder = ContextBuilder()

reflection = ReflectionEngine()

logger = MemoryLogger()


# ==================================================
# Health Check
# ==================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify(
        {
            "status": "healthy",
            "service": "Conversational Memory System",
        }
    )


# ==================================================
# Store Memory
# ==================================================

@app.route("/memory", methods=["POST"])
@login_required
def add_memory():

    data = request.get_json()

    if not data:

        return jsonify(
            {
                "error": "Invalid JSON"
            }
        ), 400

    text = data.get("text")

    if not text:

        return jsonify(
            {
                "error": "Text is required"
            }
        ), 400

    memory_type = data.get(
        "memory_type",
        "conversation",
    )

    importance = float(
        data.get(
            "importance",
            0.5,
        )
    )

    confidence = float(
        data.get(
            "confidence",
            0.9,
        )
    )

    user_id = request.user["user_id"]

    embedding = embedding_model.encode(
        text
    ).tolist()

    if memory_store.is_duplicate(
        user_id,
        embedding,
    ):

        return jsonify(
            {
                "message": "Duplicate memory ignored"
            }
        )

    memory_id = memory_store.add_memory(
        user_id=user_id,
        text=text,
        embedding=embedding,
        memory_type=memory_type,
        importance=importance,
        confidence=confidence,
    )

    logger.log_memory_added(
        user_id,
        memory_id,
        memory_type,
    )

    return jsonify(
        {
            "memory_id": memory_id,
            "status": "stored",
        }
    )


# ==================================================
# Retrieve Memories
# ==================================================

@app.route("/retrieve", methods=["POST"])
@login_required
def retrieve_memory():

    data = request.get_json()

    if not data:

        return jsonify(
            {
                "error": "Invalid JSON"
            }
        ), 400

    query = data.get("query")

    if not query:

        return jsonify(
            {
                "error": "Query is required"
            }
        ), 400

    user_id = request.user["user_id"]

    top_k = int(
        data.get(
            "top_k",
            5,
        )
    )

    memories = retriever.retrieve(
        query=query,
        user_id=user_id,
        top_k=top_k,
    )

    ranked = ranker.rank(
        memories
    )

    logger.log_retrieval(
        user_id,
        query,
        len(ranked),
    )

    return jsonify(ranked)


# ==================================================
# Build Prompt
# ==================================================

@app.route("/context", methods=["POST"])
@login_required
def build_context():

    data = request.get_json()

    if not data:

        return jsonify(
            {
                "error": "Invalid JSON"
            }
        ), 400

    query = data.get("query")

    if not query:

        return jsonify(
            {
                "error": "Query is required"
            }
        ), 400

    user_id = request.user["user_id"]

    memories = retriever.retrieve(
        query=query,
        user_id=user_id,
        top_k=10,
    )

    ranked = ranker.rank(
        memories
    )

    prompt = builder.build_prompt(
        query,
        ranked,
    )

    stats = builder.get_stats(
        prompt
    )

    return jsonify(
        {
            "prompt": prompt,
            "stats": stats,
        }
    )


# ==================================================
# Reflection
# ==================================================

@app.route("/reflection", methods=["POST"])
@login_required
def run_reflection():

    user_id = request.user["user_id"]

    summary = reflection.run(
        user_id
    )

    logger.log_reflection(
        user_id,
        summary,
    )

    return jsonify(summary)


# ==================================================
# List Memories
# ==================================================

@app.route("/memories", methods=["GET"])
@login_required
def list_memories():

    user_id = request.user["user_id"]

    memories = memory_store.list_memories(
        user_id
    )

    return jsonify(memories)


# ==================================================
# Delete Memory
# ==================================================

@app.route("/memory/<memory_id>", methods=["DELETE"])
@login_required
def delete_memory(memory_id):

    success = memory_store.delete_memory(
        memory_id
    )

    if not success:

        return jsonify(
            {
                "error": "Memory not found"
            }
        ), 404

    logger.log_memory_deleted(
        request.user["user_id"],
        memory_id,
    )

    return jsonify(
        {
            "status": "deleted"
        }
    )


# ==================================================
# Main
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )