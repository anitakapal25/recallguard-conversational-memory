POST /chat

input
{
  "user_id":"123",
  "message":"I love cricket"
}

output
{
  "response":"Got it! I'll remember that."
}

GET /memory/{user_id}

Returns all memories.

DELETE /memory/{id}

Deletes memory.

PUT /memory/{id}

Updates memory.

GET /health

Health check.