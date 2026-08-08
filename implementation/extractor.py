"""
extractor.py

Extract candidate memories from user conversation.
"""

import re
from typing import List

from models import Memory


class MemoryExtractor:
    """
    Rule-based memory extractor.

    Later this can be replaced with an LLM.
    """

    PREFERENCE_PATTERNS = [
        r"\bI like\b",
        r"\bI love\b",
        r"\bI prefer\b",
        r"\bMy favorite\b",
    ]

    FACT_PATTERNS = [
        r"\bI am\b",
        r"\bI work\b",
        r"\bI live\b",
        r"\bMy name\b",
    ]

    TASK_PATTERNS = [
        r"\bRemember\b",
        r"\bDon't forget\b",
        r"\bRemind me\b",
    ]

    def classify(self, text: str) -> str:
        text = text.strip()

        for pattern in self.PREFERENCE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return "preference"

        for pattern in self.FACT_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return "fact"

        for pattern in self.TASK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return "task"

        return "conversation"

    def split_sentences(self, text: str) -> List[str]:
        return [
            sentence.strip()
            for sentence in re.split(r"[.!?]", text)
            if sentence.strip()
        ]

    def extract(self, conversation: str) -> List[dict]:
        """
        Returns list of candidate memories.

        Example:
        [
            {
                "content":"I like coffee",
                "memory_type":"preference"
            }
        ]
        """

        memories = []

        for sentence in self.split_sentences(conversation):

            memories.append(
                {
                    "content": sentence,
                    "memory_type": self.classify(sentence),
                }
            )

        return memories