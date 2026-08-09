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

        if not query or not query.strip():
            return []

        # ----------------------------------------------
        # Generate query embedding
        # ----------------------------------------------

        embedding = self.model.encode(
            query
        ).tolist()

        # ----------------------------------------------
        # Retrieve from ChromaDB
        # ----------------------------------------------

        results = self.store.retrieve_memory(
            user_id=user_id,
            embedding=embedding,
            top_k=max(top_k * 5, 50),
        )

        # Debug information
        print("\nRETRIEVAL QUERY:", query)
        print("RETRIEVAL USER:", user_id)
        print("RETRIEVAL RAW RESULT:", results)

        memories = []

        ids = results.get(
            "ids",
            [[]]
        )[0]

        docs = results.get(
            "documents",
            [[]]
        )[0]

        metas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        # ----------------------------------------------
        # Process results
        # ----------------------------------------------

        for memory_id, doc, meta, distance in zip(
            ids,
            docs,
            metas,
            distances,
        ):

            if not meta:
                continue

            # Ignore deleted memories
            if meta.get(
                "deleted",
                False,
            ):
                continue

            # Confidence filter
            if (
                meta.get(
                    "confidence",
                    0,
                )
                < min_confidence
            ):
                continue

            # Memory type filter
            if (
                memory_type is not None
                and meta.get(
                    "memory_type"
                )
                != memory_type
            ):
                continue

            # ------------------------------------------
            # Convert Chroma L2 distance
            # to cosine similarity
            #
            # For normalized embeddings:
            #
            # cosine similarity =
            # 1 - (L2 distance / 2)
            # ------------------------------------------

            similarity = 1.0 - (
                distance / 2.0
            )

            similarity = max(
                0.0,
                min(
                    1.0,
                    similarity,
                ),
            )

            print(
                "MEMORY:",
                doc,
                "| distance:",
                distance,
                "| similarity:",
                similarity,
            )

            # ------------------------------------------
            # Ignore weak matches
            # ------------------------------------------

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

        # ----------------------------------------------
        # Sort by relevance
        # ----------------------------------------------

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

        ids = results.get(
            "ids",
            []
        )

        docs = results.get(
            "documents",
            []
        )

        metas = results.get(
            "metadatas",
            []
        )

        for memory_id, doc, meta in zip(
            ids,
            docs,
            metas,
        ):

            if not meta:
                continue

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