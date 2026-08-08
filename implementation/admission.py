"""
admission.py

Admission policy for memories.
"""

from typing import Dict


class AdmissionEngine:

    IMPORTANT_WORDS = [
        "always",
        "never",
        "important",
        "remember",
        "favorite",
        "prefer",
    ]

    def importance_score(self, text: str) -> float:

        score = 0.4

        words = text.lower()

        for word in self.IMPORTANT_WORDS:
            if word in words:
                score += 0.1

        return min(score, 1.0)

    def confidence_score(self, text: str) -> float:

        if len(text) < 5:
            return 0.3

        return 0.9

    def should_store(self, text: str) -> bool:

        if len(text.strip()) < 5:
            return False

        if text.isnumeric():
            return False

        return True

    def evaluate(self, memory: Dict) -> Dict:

        content = memory["content"]

        memory["importance"] = self.importance_score(content)
        memory["confidence"] = self.confidence_score(content)
        memory["store"] = self.should_store(content)

        return memory