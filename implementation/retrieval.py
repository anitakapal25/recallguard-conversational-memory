"""Semantic candidates with explicit filters; ranking is separate."""
from embeddings import SentenceEncoder
import re

# Exact lexical coverage rescues rare terms and long/noisy memories. Generic
# function words cannot admit a result on their own. This is not query expansion.
STOP_WORDS = {"i", "my", "me", "a", "an", "the", "is", "are", "am", "do", "does",
              "what", "which", "where", "how", "who", "user", "of", "to", "in", "for"}


class MemoryRetriever:
    def __init__(self, store, encoder=None):
        self.store = store
        self.model = encoder or SentenceEncoder()

    def retrieve(self, query, user_id, top_k=5, memory_type=None, min_confidence=0.0):
        if not query or not query.strip():
            return []
        if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 100:
            raise ValueError("top_k must be 1-100")
        results = self.store.retrieve_memory(user_id, self.model.encode(query), min(100, max(50, top_k * 5)))
        query_terms = set(re.findall(r"\w+", query.casefold())) - STOP_WORDS
        memories = []
        for mid, doc, meta, distance in zip(*(results[key][0] for key in ("ids", "documents", "metadatas", "distances"))):
            similarity = max(0.0, min(1.0, 1 - distance / 2))
            exact_coverage = bool(query_terms) and query_terms.issubset(set(re.findall(r"\w+", doc.casefold())))
            if (similarity < 0.4 and not exact_coverage) or meta.get("confidence", 0) < min_confidence:
                continue
            if memory_type is not None and meta["memory_type"] != memory_type:
                continue
            memories.append({"id": mid, "content": doc, "metadata": meta, "similarity": similarity,
                             "lexical_match": exact_coverage})
        return sorted(memories, key=lambda m: m["similarity"], reverse=True)[:top_k]

    def _typed(self, user_id, memory_type, top_k):
        data = self.store.get_memories_by_type(user_id, memory_type)
        return [{"id": mid, "content": doc, "metadata": meta, "similarity": 1.0}
                for mid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"])][:top_k]

    def retrieve_preferences(self, user_id, top_k=5):
        return self._typed(user_id, "preference", top_k)

    def retrieve_facts(self, user_id, top_k=5):
        return self._typed(user_id, "fact", top_k)

    def retrieve_tasks(self, user_id, top_k=5):
        return self._typed(user_id, "task", top_k)
