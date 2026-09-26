"""Idempotent, owner-scoped maintenance. Called by API or maintenance worker."""
from collections import Counter
from memory_store import MemoryStore


class ReflectionEngine:
    def __init__(self, collection_name="conversation_memory", store=None):
        self.store = store or MemoryStore(collection_name)

    def run(self, user_id):
        expired = self.store.expire_memories(user_id)
        data = self.store.list_memories(user_id)
        seen = set()
        duplicates = low_confidence = 0
        for mid, text, meta in zip(data["ids"], data["documents"], data["metadatas"]):
            key = (meta["memory_type"], text.strip().casefold())
            if meta["confidence"] < 0.3:
                low_confidence += int(self.store.delete_memory(mid, user_id))
            elif key in seen:
                duplicates += int(self.store.delete_memory(mid, user_id))
            else:
                seen.add(key)
        remaining = self.store.list_memories(user_id)
        counts = Counter(m["memory_type"] for m in remaining["metadatas"])
        return {"user_id": user_id, "summary": {"total": len(remaining["ids"]), **counts},
                "maintenance": {"expired": expired, "duplicates_removed": duplicates,
                                "low_confidence_removed": low_confidence}}
