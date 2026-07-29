def build_prompt(memories, current_question):

    memory_text = "\n".join(memories)

    prompt = f"""
You are a helpful assistant.

Relevant memories:

{memory_text}

Current user question:

{current_question}

Answer the user's question using the relevant memories when appropriate.
"""

    return prompt