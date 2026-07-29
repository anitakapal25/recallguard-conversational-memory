import uuid

from implementation.database import collection


def store_memory(user_id, text, embedding):

    collection.add(

        ids=[str(uuid.uuid4())],

        documents=[text],

        embeddings=[embedding],

        metadatas=[
            {
                "user_id": user_id
            }
        ]
    )


def retrieve_memory(user_id, embedding, top_k=5):

    result = collection.query(

        query_embeddings=[embedding],

        n_results=top_k,

        where={
            "user_id": user_id
        }

    )

    return result