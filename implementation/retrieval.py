"""
retrieval.py

Memory retrieval layer using ChromaDB.
"""

from typing import Dict, List, Optional

from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL
from memory_store import MemoryStore


class MemoryRetriever:

    def __init__(self, store: MemoryStore):
        self.store = store
        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    # --------------------------------------------------
    # General Retrieval
    # --------------------------------------------------

    def retrieve(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        memory_type: Optional[str] = None,
        min_confidence: float = 0.0,
    ) -> List[Dict]:

        # Empty query used for filtering
        if query.strip():

            embedding = self.model.encode(
                query
            ).tolist()

        else:

            embedding = self.model.encode(
                "memory"
            ).tolist()

        # Retrieve more than required so filtering
        # doesn't accidentally remove all results
        results = self.store.retrieve_memory(
            user_id=user_id,
            embedding=embedding,
            top_k=max(top_k * 5, 50),
        )

        memories = []

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for memory_id, doc, meta, distance in zip(
            ids,
            docs,
            metas,
            distances,
        ):

            if meta.get("deleted", False):
                continue

            if (
                meta.get("confidence", 0)
                < min_confidence
            ):
                continue

            if (
                memory_type is not None
                and meta.get("memory_type")
                != memory_type
            ):
                continue

            similarity = max(
                0.0,
                1.0 - distance,
            )

            # Ignore weak matches
            if similarity < 0.40:
                continue

            memories.append(
                {
                    "id": memory_id,
                    "content": doc,
                    "similarity": similarity,
                    "metadata": meta,
                }
            )

        memories.sort(
            key=lambda x: x["similarity"],
            reverse=True,
        )

        return memories[:top_k]

    # --------------------------------------------------
    # Retrieve Preferences
    # --------------------------------------------------

    def retrieve_preferences(
        self,
        user_id: str,
        top_k: int = 5,
    ) -> List[Dict]:

        results = self.store.get_memories_by_type(
            user_id,
            "preference",
        )

        return self._convert_results(
            results,
            top_k,
        )

    # --------------------------------------------------
    # Retrieve Facts
    # --------------------------------------------------

    def retrieve_facts(
        self,
        user_id: str,
        top_k: int = 5,
    ) -> List[Dict]:

        results = self.store.get_memories_by_type(
            user_id,
            "fact",
        )

        return self._convert_results(
            results,
            top_k,
        )

    # --------------------------------------------------
    # Retrieve Tasks
    # --------------------------------------------------

    def retrieve_tasks(
        self,
        user_id: str,
        top_k: int = 5,
    ) -> List[Dict]:

        results = self.store.get_memories_by_type(
            user_id,
            "task",
        )

        return self._convert_results(
            results,
            top_k,
        )

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def _convert_results(
        self,
        results,
        top_k,
    ) -> List[Dict]:

        memories = []

        ids = results.get("ids", [])
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])

        for memory_id, doc, meta in zip(
            ids,
            docs,
            metas,
        ):

            if meta.get(
                "deleted",
                False,
            ):
                continue

            memories.append(
                {
                    "id": memory_id,
                    "content": doc,
                    "similarity": 1.0,
                    "metadata": meta,
                }
            )

        return memories[:top_k]