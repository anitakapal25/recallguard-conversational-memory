"""
reflection.py

Background reflection and maintenance
for the Conversational Memory System.
"""

from datetime import datetime, timedelta, timezone

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
            "goal": 0,
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
        user_id: str,
        days: int = 365,
    ):

        memories = self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            },
            include=["metadatas"],
        )

        expiry = (
            datetime.now(timezone.utc).replace(tzinfo=None)
            - timedelta(days=days)
        )

        expired_count = 0

        for memory_id, meta in zip(
            memories.get("ids", []),
            memories.get("metadatas", []),
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
            except (ValueError, TypeError):
                continue

            if created < expiry:

                meta["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[meta],
                )

                expired_count += 1

        return expired_count

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
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        seen = set()
        duplicate_count = 0

        for memory_id, doc, meta in zip(
            memories.get("ids", []),
            memories.get("documents", []),
            memories.get("metadatas", []),
        ):

            if not doc:
                continue

            key = doc.strip().lower()

            if key in seen:

                meta["deleted"] = True

                self.collection.update(
                    ids=[memory_id],
                    metadatas=[meta],
                )

                duplicate_count += 1

            else:

                seen.add(key)

        return duplicate_count

    # --------------------------------------------------
    # Remove Low Confidence Memories
    # --------------------------------------------------

    def remove_low_confidence(
        self,
        user_id: str,
        threshold: float = 0.30,
    ):

        memories = self.collection.get(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"deleted": False},
                ]
            },
            include=["metadatas"],
        )

        removed_count = 0

        for memory_id, meta in zip(
            memories.get("ids", []),
            memories.get("metadatas", []),
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

                removed_count += 1

        return removed_count

    # --------------------------------------------------
    # Run Reflection
    # --------------------------------------------------

    def run(
        self,
        user_id: str,
    ):

        expired = self.expire_memories(
            user_id
        )

        duplicates = self.remove_duplicates(
            user_id
        )

        low_confidence = (
            self.remove_low_confidence(
                user_id
            )
        )

        summary = self.summarize(
            user_id
        )

        return {
            "user_id": user_id,
            "summary": summary,
            "maintenance": {
                "expired": expired,
                "duplicates_removed": duplicates,
                "low_confidence_removed": (
                    low_confidence
                ),
            },
        }


# ==================================================
# Manual Test
# ==================================================

if __name__ == "__main__":

    reflection = ReflectionEngine()

    user_id = "user_1"

    result = reflection.run(
        user_id
    )

    print("\nReflection Result:")
    print(result)