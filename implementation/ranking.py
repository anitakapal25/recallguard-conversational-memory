"""
ranking.py

Ranks retrieved memories using multiple signals.
"""

from datetime import datetime
from typing import Dict, List


class MemoryRanker:

    def __init__(
        self,
        similarity_weight: float = 0.50,
        importance_weight: float = 0.20,
        confidence_weight: float = 0.20,
        recency_weight: float = 0.10,
    ):

        self.similarity_weight = similarity_weight
        self.importance_weight = importance_weight
        self.confidence_weight = confidence_weight
        self.recency_weight = recency_weight

    # --------------------------------------------------

    def recency_score(
        self,
        created_at: str,
    ) -> float:

        try:
            created = datetime.fromisoformat(
                created_at
            )

            age = (
                datetime.utcnow() - created
            ).days

        except Exception:
            return 0.5

        if age <= 1:
            return 1.0
        elif age <= 7:
            return 0.9
        elif age <= 30:
            return 0.8
        elif age <= 90:
            return 0.6
        elif age <= 180:
            return 0.4

        return 0.2

    # --------------------------------------------------

    def score(
        self,
        memory: Dict,
    ) -> float:

        metadata = memory["metadata"]

        similarity = memory.get(
            "similarity",
            0,
        )

        importance = metadata.get(
            "importance",
            0.5,
        )

        confidence = metadata.get(
            "confidence",
            0.5,
        )

        recency = self.recency_score(
            metadata.get(
                "created_at",
                "",
            )
        )

        return (
            self.similarity_weight * similarity
            + self.importance_weight * importance
            + self.confidence_weight * confidence
            + self.recency_weight * recency
        )

    # --------------------------------------------------

    def rank(
        self,
        memories: List[Dict],
    ) -> List[Dict]:

        ranked = sorted(
            memories,
            key=self.score,
            reverse=True,
        )

        return ranked

    # --------------------------------------------------

    def explain(
        self,
        memory: Dict,
    ) -> Dict:

        metadata = memory["metadata"]

        return {
            "similarity": memory.get(
                "similarity",
                0,
            ),
            "importance": metadata.get(
                "importance",
                0,
            ),
            "confidence": metadata.get(
                "confidence",
                0,
            ),
            "recency": self.recency_score(
                metadata.get(
                    "created_at",
                    "",
                )
            ),
            "final_score": round(
                self.score(memory),
                4,
            ),
        }