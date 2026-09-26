"""Owner-scoped Chroma storage. Physical API deletion is not forensic erasure."""
import math
import uuid
from datetime import datetime, timedelta, timezone
from database import get_collection

TYPES = {"conversation", "preference", "fact", "goal", "task"}


def utcnow():
    return datetime.now(timezone.utc)


def parse_time(value):
    result = datetime.fromisoformat(value)
    return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result


class MemoryStore:
    def __init__(self, collection_name="conversation_memory", *, collection=None, path=None, clock=utcnow):
        self.collection = collection if collection is not None else get_collection(collection_name, path)
        self.clock = clock

    def active(self, meta):
        if meta.get("deleted", False):
            return False
        try:
            return not meta.get("expires_at") or parse_time(meta["expires_at"]) > self.clock()
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _validate(text, memory_type, importance, confidence):
        if not isinstance(text, str) or not text.strip() or len(text) > 4000:
            raise ValueError("text must contain 1-4000 characters")
        if not isinstance(memory_type, str) or memory_type not in TYPES:
            raise ValueError("unsupported memory_type")
        for value in (importance, confidence):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError("importance and confidence must be finite numbers from 0 to 1")

    def add_memory(self, user_id, text, embedding, memory_type="conversation", importance=0.5,
                   confidence=0.9, *, source="manual", conversation_id="", retention_days=7):
        self._validate(text, memory_type, importance, confidence)
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id is required")
        if not isinstance(retention_days, int) or isinstance(retention_days, bool) or not 1 <= retention_days <= 7:
            raise ValueError("retention_days must be 1-7")
        now = self.clock()
        memory_id = str(uuid.uuid4())
        self.collection.add(ids=[memory_id], documents=[text], embeddings=[embedding], metadatas=[{
            "user_id": user_id, "memory_type": memory_type, "importance": float(importance),
            "confidence": float(confidence), "created_at": now.isoformat(), "updated_at": now.isoformat(),
            "expires_at": (now + timedelta(days=retention_days)).isoformat(),
            "source": source, "conversation_id": conversation_id, "version": 1, "deleted": False,
        }])
        return memory_id

    def get_memory(self, memory_id, user_id):
        return self._filter(self.collection.get(ids=[memory_id], where={"user_id": user_id}))

    def _filter(self, result):
        indices = [i for i, meta in enumerate(result.get("metadatas", [])) if self.active(meta)]
        return {key: [result[key][i] for i in indices] for key in ("ids", "documents", "metadatas")}

    def list_memories(self, user_id):
        return self._filter(self.collection.get(where={"user_id": user_id}))

    def delete_memory(self, memory_id, user_id):
        result = self.collection.get(ids=[memory_id], where={"user_id": user_id})
        if not result["ids"]:
            return False
        self.collection.delete(ids=[memory_id], where={"user_id": user_id})
        return True

    def update_memory(self, memory_id, new_text, new_embedding, user_id, *, source="manual-correction"):
        record = self.get_memory(memory_id, user_id)
        if not record["ids"]:
            return False
        meta = record["metadatas"][0]
        self._validate(new_text, meta["memory_type"], meta["importance"], meta["confidence"])
        meta.update(updated_at=self.clock().isoformat(), source=source, version=meta.get("version", 1) + 1)
        self.collection.update(ids=[memory_id], documents=[new_text], embeddings=[new_embedding], metadatas=[meta])
        return True

    def retrieve_memory(self, user_id, embedding, top_k=5):
        if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 100:
            raise ValueError("top_k must be 1-100")
        active_ids = self.list_memories(user_id)["ids"]
        if not active_ids:
            return {key: [[]] for key in ("ids", "documents", "metadatas", "distances")}
        return self.collection.query(query_embeddings=[embedding], n_results=min(top_k, len(active_ids)),
            ids=active_ids, where={"user_id": user_id}, include=["documents", "metadatas", "distances"])

    def is_duplicate(self, tenant_id, embedding, threshold=0.95):
        result = self.retrieve_memory(tenant_id, embedding, 1)
        distances = result["distances"][0]
        return bool(distances and 1 - distances[0] / 2 >= threshold)

    def get_memories_by_type(self, user_id, memory_type):
        data = self.list_memories(user_id)
        indices = [i for i, m in enumerate(data["metadatas"]) if m["memory_type"] == memory_type]
        return {key: [values[i] for i in indices] for key, values in data.items()}

    def expire_memories(self, user_id):
        result = self.collection.get(where={"user_id": user_id})
        expired = [mid for mid, meta in zip(result["ids"], result["metadatas"]) if not self.active(meta)]
        if expired:
            self.collection.delete(ids=expired, where={"user_id": user_id})
        return len(expired)
