"""
admission.py

Admission policy for memories.

Determines whether an extracted memory should
be stored as long-term memory.
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

    # ==================================================
    # Importance
    # ==================================================

    def importance_score(
        self,
        text: str,
    ) -> float:

        score = 0.4

        words = text.lower()

        for word in self.IMPORTANT_WORDS:

            if word in words:
                score += 0.1

        return min(score, 1.0)

    # ==================================================
    # Confidence
    # ==================================================

    def confidence_score(
        self,
        text: str,
    ) -> float:

        if len(text.strip()) < 5:
            return 0.3

        return 0.9

    # ==================================================
    # Should Store
    # ==================================================

    def should_store(
        self,
        text: str,
    ) -> bool:

        text = text.strip()

        if len(text) < 10:
            return False

        if text.isnumeric():
            return False

        conversation_words = [
            "hello",
            "hi",
            "hey",
            "thanks",
            "thank you",
            "okay",
            "ok",
        ]

        if text.lower().strip("!.? ") in conversation_words:
            return False

        return True
    # ==================================================
    # Evaluate Memory
    # ==================================================

    def evaluate(
        self,
        memory: Dict,
    ) -> Dict:

        content = memory["content"]

        memory["importance"] = (
            self.importance_score(content)
        )

        memory["confidence"] = (
            self.confidence_score(content)
        )

        memory["store"] = (
            self.should_store(content)
        )

        return memory


# ==================================================
# Manual Test
# ==================================================

if __name__ == "__main__":

    admission = AdmissionEngine()

    test_memories = [
        {
            "memory_type": "preference",
            "content": "I prefer coffee.",
        },
        {
            "memory_type": "goal",
            "content": "I want to become an AI Engineer.",
        },
        {
            "memory_type": "conversation",
            "content": "Hello.",
        },
        {
            "memory_type": "conversation",
            "content": "12345",
        },
    ]

    for memory in test_memories:

        result = admission.evaluate(
            memory
        )

        print("\nInput:")
        print(memory["content"])

        print("Evaluation:")
        print(result)