"""Honest append-only, owner-filtered single-similarity baseline.

It deliberately has no admission, freshness lifecycle or context allocation.
Corrections append statements. Delete/expiry intents are unsupported and recorded.
"""
import uuid


class NaiveBaseline:
    def __init__(self, collection, encoder):
        self.collection, self.encoder = collection, encoder

    def add(self, user, text):
        mid = str(uuid.uuid4())
        self.collection.add(ids=[mid], documents=[text], embeddings=[self.encoder.encode(text)],
                            metadatas=[{"user_id":user,"memory_type":"conversation"}])
        return mid

    def retrieve(self, user, query, top_k=5):
        size = len(self.collection.get(where={"user_id":user})["ids"])
        if not size:
            return []
        result = self.collection.query(query_embeddings=[self.encoder.encode(query)], where={"user_id":user},
                                       n_results=min(size, top_k), include=["documents","metadatas","distances"])
        return [{"id":mid,"content":text,"metadata":meta,"similarity":1-distance/2}
                for mid,text,meta,distance in zip(*(result[k][0] for k in ("ids","documents","metadatas","distances")))]
