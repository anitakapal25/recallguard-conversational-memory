"""
context_builder.py

Builds the context sent to the LLM from
retrieved and ranked memories.
"""

from typing import Dict, List

from config import MAX_CONTEXT_TOKENS


class ContextBuilder:

    def __init__(
        self,
        token_budget: int = MAX_CONTEXT_TOKENS,
    ):
        self.token_budget = token_budget

    # --------------------------------------------------
    # Estimate Tokens
    # --------------------------------------------------

    def estimate_tokens(
        self,
        text: str,
    ) -> int:
        """
        Approximate token count.

        Rule:
        1 token ≈ 4 characters
        """

        return max(
            1,
            len(text) // 4,
        )

    # --------------------------------------------------
    # Build Memory Context
    # --------------------------------------------------

    def build_context(
        self,
        memories: List[Dict],
    ) -> str:

        lines = []
        used_tokens = 0

        for memory in memories:

            metadata = memory["metadata"]

            line = (
                f"[{metadata['memory_type'].upper()}] "
                f"{memory['content']}"
            )

            tokens = self.estimate_tokens(
                line
            )

            if (
                used_tokens + tokens
                > self.token_budget
            ):
                break

            lines.append(line)

            used_tokens += tokens

        return "\n".join(lines)

    # --------------------------------------------------
    # Build Final Prompt
    # --------------------------------------------------

    def build_prompt(
        self,
        user_query: str,
        memories: List[Dict],
    ) -> str:

        memory_context = self.build_context(
            memories
        )

        if not memory_context:

            memory_context = (
                "No relevant memories found."
            )

        prompt = f"""
You are an AI assistant.

Relevant User Memories
----------------------
{memory_context}

Current User Query
------------------
{user_query}

Instructions
------------
1. Use memories only if they are relevant.
2. Do not invent information.
3. Prefer newer memories if conflicts exist.
4. If no memory is relevant, answer normally.
"""

        return prompt.strip()

    # --------------------------------------------------
    # Context Statistics
    # --------------------------------------------------

    def get_stats(
        self,
        context: str,
    ) -> Dict:

        tokens = self.estimate_tokens(
            context
        )

        return {
            "characters": len(context),
            "estimated_tokens": tokens,
            "budget": self.token_budget,
            "utilization": round(
                (
                    tokens
                    / self.token_budget
                )
                * 100,
                2,
            ),
        }

    # --------------------------------------------------
    # Trim Context
    # --------------------------------------------------

    def trim_context(
        self,
        memories: List[Dict],
        max_memories: int,
    ) -> List[Dict]:

        return memories[:max_memories]