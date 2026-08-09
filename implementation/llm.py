"""
llm.py

Local LLM interface using Ollama.
"""

import ollama


class LocalLLM:

    def __init__(
        self,
        model: str = "llama3.2:3b",
    ):
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]