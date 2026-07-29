from fastapi import FastAPI
from pydantic import BaseModel

from implementation.llm import create_embedding, generate_response
from implementation.memory import store_memory, retrieve_memory
from implementation.prompt import build_prompt

app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    # Create embedding
    embedding = create_embedding(request.message)

    # Store memory
    store_memory(
        request.user_id,
        request.message,
        embedding
    )

    # Retrieve similar memories
    memories = retrieve_memory(
        request.user_id,
        embedding
    )

    memory_list = memories["documents"][0]

    # Build prompt
    prompt = build_prompt(
        memory_list,
        request.message
    )

    # Generate AI response
    answer = generate_response(prompt)

    return {
        "current_message": request.message,
        "retrieved_memories": memory_list,
        "answer": answer
    }