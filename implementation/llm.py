from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    return embedding_model.encode(text).tolist()


def generate_response(prompt):

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]