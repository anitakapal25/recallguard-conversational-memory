"""
reflection.py

Background reflection and maintenance
for the Conversational Memory System.
"""

from datetime import datetime, timedelta

from database import get_collection


class ReflectionEngine:

    def __init__(
        self,
        collection_name: str = "conversation_memory",
    ):
        self.collection = get_collection(
            collection_name
        )

    # --------------------------------------------------
    # Reflection Summary
    # --------------------------------------------------

    def summarize(
        self,
        user_id: str,
    ):

        memories = self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            }
        )

        summary = {
            "total": 0,
            "preference": 0,
            "fact": 0,
            "task": 0,
            "conversation": 0,
        }

        for meta in memories.get(
            "metadatas",
            [],
        ):

            summary["total"] += 1

            memory_type = meta.get(
                "memory_type",
                "conversation",
            )

            if memory_type in summary:
                summary[memory_type] += 1
            else:
                summary["conversation"] += 1

        return summary

    # --------------------------------------------------
    # Expire Old Memories
    # --------------------------------------------------

    def expire_memories(
        self,
        days: int = 365,
    ):

        memories = self.collection.get(
            include=["metadatas"]
        )

        expiry = (
            datetime.utcnow()
            - timedelta(days=days)
        )

        for memory_id, meta in zip(
            memories["ids"],
            memories["metadatas"],
        ):

            created = meta.get(
                "created_at"
            )

            if not created:
                continue

            try:
                created = datetime.fromisoformat(
                    created
                )
            except ValueError:
                continue

            if created < expiry:

                meta["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[meta],
                )

    # --------------------------------------------------
    # Remove Duplicate Memories
    # --------------------------------------------------

    def remove_duplicates(
        self,
        user_id: str,
    ):

        memories = self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            }
        )

        seen = set()

        for memory_id, doc, meta in zip(
            memories["ids"],
            memories["documents"],
            memories["metadatas"],
        ):

            key = doc.strip().lower()

            if key in seen:

                meta["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[meta],
                )

            else:

                seen.add(key)

    # --------------------------------------------------
    # Remove Low Confidence Memories
    # --------------------------------------------------

    def remove_low_confidence(
        self,
        threshold: float = 0.30,
    ):

        memories = self.collection.get(
            include=["metadatas"]
        )

        for memory_id, meta in zip(
            memories["ids"],
            memories["metadatas"],
        ):

            confidence = meta.get(
                "confidence",
                1.0,
            )

            if confidence < threshold:

                meta["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[meta],
                )

    # --------------------------------------------------
    # Run Reflection
    # --------------------------------------------------

    def run(
        self,
        user_id: str,
    ):

        self.expire_memories()

        self.remove_duplicates(
            user_id
        )

        self.remove_low_confidence()

        return self.summarize(
            user_id
        )