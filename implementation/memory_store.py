"""
memory_store.py

Deliverable 6
Persistent memory store using ChromaDB.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from database import get_collection


class MemoryStore:

    def __init__(
        self,
        collection_name="conversation_memory",
    ):
        self.collection = get_collection(
            collection_name
        )
    # --------------------------------------------------
    # Add Memory
    # --------------------------------------------------

    def add_memory(
        self,
        user_id: str,
        text: str,
        embedding,
        memory_type: str = "conversation",
        importance: float = 0.5,
        confidence: float = 0.9,
    ) -> str:

        memory_id = str(uuid.uuid4())

        self.collection.add(
            ids=[memory_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[
                {
                    "user_id": user_id,
                    "memory_type": memory_type,
                    "importance": importance,
                    "confidence": confidence,
                    "created_at": datetime.utcnow().isoformat(),
                    "deleted": False,
                }
            ],
        )

        return memory_id

    # --------------------------------------------------
    # Retrieve Memories
    # --------------------------------------------------

    def retrieve_memory(
        self,
        user_id: str,
        embedding,
        top_k: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            },
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    # --------------------------------------------------
    # Get Memory By ID
    # --------------------------------------------------

    def get_memory(
        self,
        memory_id: str,
    ):

        return self.collection.get(
            ids=[memory_id],
        )

    # --------------------------------------------------
    # List User Memories
    # --------------------------------------------------

    def list_memories(
        self,
        user_id: str,
    ):

        return self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            }
        )

    # --------------------------------------------------
    # Soft Delete
    # --------------------------------------------------

    def delete_memory(
        self,
        memory_id: str,
    ):

        memory = self.collection.get(
            ids=[memory_id],
            include=["metadatas"],
        )

        if not memory["ids"]:
            return False

        metadata = memory["metadatas"][0]

        metadata["deleted"] = True

        self.collection.update(
            ids=[memory_id],
            metadatas=[metadata],
        )

        return True

    # --------------------------------------------------
    # Update Memory
    # --------------------------------------------------

    def update_memory(
        self,
        memory_id: str,
        new_text: str,
        new_embedding,
    ):

        self.collection.update(
            ids=[memory_id],
            documents=[new_text],
            embeddings=[new_embedding],
        )

        return True

    # --------------------------------------------------
    # Duplicate Detection
    # --------------------------------------------------

    def is_duplicate(
        self,
        tenant_id,
        embedding,
        threshold=0.85,
    ):
        """
        Check whether a very similar memory already exists.

        Uses ChromaDB distance and converts squared L2
        distance to cosine similarity for normalized embeddings.

        Returns:
            True  -> duplicate found
            False -> no duplicate found
        """

        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=1,
            where={
                "$and": [
                    {"user_id": tenant_id},
                    {"deleted": False},
                ]
            },
            include=["distances"],
        )
        print("DUPLICATE QUERY RESULT:", result)

        # No existing memories
        if (
            not result
            or not result.get("distances")
            or not result["distances"][0]
        ):
            return False

        distance = result["distances"][0][0]

        # Chroma's default L2 distance for normalized vectors:
        # cosine_similarity = 1 - (distance / 2)
        print("DUPLICATE CHECK DISTANCE:", distance)

        similarity = 1 - (distance / 2)

        print("DUPLICATE CHECK SIMILARITY:", similarity)

        return similarity >= threshold
    # --------------------------------------------------
    # Expire Memories
    # --------------------------------------------------

    def expire_memories(
        self,
        expiry_days: int = 365,
    ):

        memories = self.collection.get(
            include=["metadatas"]
        )

        now = datetime.utcnow()

        for memory_id, metadata in zip(
            memories["ids"],
            memories["metadatas"],
        ):

            created = datetime.fromisoformat(
                metadata["created_at"]
            )

            age = (now - created).days

            if age > expiry_days:

                metadata["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[metadata],
                )

    # --------------------------------------------------
    # Get Memories By Type
    # --------------------------------------------------

    def get_memories_by_type(
        self,
        user_id: str,
        memory_type: str,
    ):

        return self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"memory_type": memory_type},
                    {"deleted": False},
                ]
            },
        )