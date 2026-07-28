from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="RecallGuard Memory Service",
    version="1.0"
)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "RecallGuard Conversational Memory"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    return {
        "user": request.user_id,
        "message": request.message,
        "reply": "This is a placeholder response."
    }