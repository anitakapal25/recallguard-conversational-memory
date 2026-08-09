"""
extractor.py

Extracts potentially useful long-term memories
from conversational text.

This is a lightweight rule-based extractor designed
for the RecallGuard project.

It identifies:
- Preferences
- Goals
- Facts
- Important personal information
- Explicit dislikes

It does NOT use a paid LLM/API.
"""

import re
from typing import List, Dict


class MemoryExtractor:

    def __init__(self):
        pass

    # ==================================================
    # Main Extraction Method
    # ==================================================

    def extract(
        self,
        text: str,
    ) -> List[Dict]:

        if not text:
            return []

        text = text.strip()

        if not text:
            return []

        memories = []

        # --------------------------------------------------
        # Preference
        # --------------------------------------------------

        preference_patterns = [
            r"\bi (?:really\s+)?(?:like|love|prefer|enjoy)\s+(.+)",
            r"\bi(?:'m| am) a fan of\s+(.+)",
            r"\bmy favorite\s+(.+?)\s+is\s+(.+)",
        ]

        for pattern in preference_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                memories.append(
                    {
                        "memory_type": "preference",
                        "content": text,
                        "importance": 0.6,
                        "confidence": 0.9,
                    }
                )

                break

        # --------------------------------------------------
        # Goal
        # --------------------------------------------------

        goal_patterns = [
            r"\bi want to\s+(.+)",
            r"\bi would like to\s+(.+)",
            r"\bmy goal is to\s+(.+)",
            r"\bi(?:'m| am) planning to\s+(.+)",
            r"\bi hope to\s+(.+)",
        ]

        for pattern in goal_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                memories.append(
                    {
                        "memory_type": "goal",
                        "content": text,
                        "importance": 0.8,
                        "confidence": 0.9,
                    }
                )

                break

        # --------------------------------------------------
        # Explicit dislike
        # --------------------------------------------------

        dislike_patterns = [
            r"\bi (?:don't|do not) like\s+(.+)",
            r"\bi hate\s+(.+)",
            r"\bi dislike\s+(.+)",
            r"\bi avoid\s+(.+)",
        ]

        for pattern in dislike_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                memories.append(
                    {
                        "memory_type": "preference",
                        "content": text,
                        "importance": 0.7,
                        "confidence": 0.9,
                    }
                )

                break

        # --------------------------------------------------
        # Personal facts
        # --------------------------------------------------

        fact_patterns = [
            r"\bi work at\s+(.+)",
            r"\bi work as\s+(.+)",
            r"\bi live in\s+(.+)",
            r"\bi am from\s+(.+)",
            r"\bi have\s+(.+)",
            r"\bi use\s+(.+)",
            r"\bi(?:'m| am) learning\s+(.+)",
        ]

        for pattern in fact_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:

                memories.append(
                    {
                        "memory_type": "fact",
                        "content": text,
                        "importance": 0.6,
                        "confidence": 0.85,
                    }
                )

                break

        # --------------------------------------------------
        # Remove duplicate extracted memories
        # --------------------------------------------------

        unique_memories = []

        seen = set()

        for memory in memories:

            key = (
                memory["memory_type"],
                memory["content"].lower().strip(),
            )

            if key not in seen:

                seen.add(key)

                unique_memories.append(
                    memory
                )

        return unique_memories


# ==================================================
# Convenience Function
# ==================================================

def extract_memories(
    text: str,
) -> List[Dict]:

    extractor = MemoryExtractor()

    return extractor.extract(text)


# ==================================================
# Manual Test
# ==================================================

if __name__ == "__main__":

    extractor = MemoryExtractor()

    examples = [
        "I like coffee.",
        "I want to become an AI Engineer.",
        "I am learning Python.",
        "I live in Bangalore.",
        "I don't like tea.",
        "Hello, how are you?",
        "I really enjoy drinking coffee.",
    ]

    for example in examples:

        print("\nInput:")
        print(example)

        print("Extracted:")

        results = extractor.extract(
            example
        )

        for result in results:
            print(result)