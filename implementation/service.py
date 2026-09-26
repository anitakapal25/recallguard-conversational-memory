"""Shared application policies; every text write passes through this boundary."""
from threading import RLock
from admission import AdmissionEngine
from extractor import MemoryExtractor
from pii_filter import PIIFilter
from retrieval import MemoryRetriever
from ranking import MemoryRanker
from context_builder import ContextBuilder
from reflection import ReflectionEngine


class MemoryService:
    def __init__(self, store, encoder, llm=None, builder=None):
        self.store, self.encoder, self.llm = store, encoder, llm
        self.retriever = MemoryRetriever(store, encoder)
        self.ranker = MemoryRanker()
        self.builder = builder or ContextBuilder()
        self.pii = PIIFilter()
        self.extractor, self.admission = MemoryExtractor(), AdmissionEngine()
        self.lock = RLock()  # single-process local deployment; not a distributed lock

    @staticmethod
    def text(value):
        if not isinstance(value, str) or not value.strip() or len(value) > 4000:
            raise ValueError("text must contain 1-4000 characters")
        return value.strip()

    def safe_text(self, text):
        text = self.text(text)
        if self.pii.contains_pii(text):
            raise ValueError("sensitive content rejected by admission policy")
        return text

    def add(self, user_id, text, *, memory_type="conversation", importance=0.5,
            confidence=0.9, source="manual", conversation_id="", retention_days=7):
        text = self.safe_text(text)
        self.store._validate(text, memory_type, importance, confidence)
        with self.lock:
            # Conservative exact duplicate admission avoids dropping changed preferences
            # merely because their embeddings are close.
            records = self.store.list_memories(user_id)
            for mid, doc, meta in zip(records["ids"], records["documents"], records["metadatas"]):
                if doc.casefold().strip() == text.casefold() and meta["memory_type"] == memory_type:
                    return {"status": "duplicate", "memory_id": mid}
            embedding = self.encoder.encode(text)
            mid = self.store.add_memory(user_id, text, embedding, memory_type, importance, confidence,
                source=source, conversation_id=conversation_id, retention_days=retention_days)
        return {"status": "stored", "memory_id": mid}

    def correct(self, user_id, mid, text):
        text = self.safe_text(text)
        with self.lock:
            if not self.store.get_memory(mid, user_id)["ids"]:
                return False
            return self.store.update_memory(mid, text, self.encoder.encode(text), user_id)

    def retrieve(self, user_id, query, top_k=5):
        query = self.safe_text(query)
        if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 20:
            raise ValueError("top_k must be 1-20")
        candidates = self.retriever.retrieve(query, user_id, top_k=100)
        return self.ranker.rank(candidates)[:top_k]

    def chat(self, user_id, message, remember=False, conversation_id=""):
        message = self.safe_text(message)
        # Reject oversize prompts BEFORE committing memory.
        self.builder.build_prompt(message, [])
        decisions = []
        if remember:
            for memory in self.extractor.extract(message):
                result = self.admission.evaluate(memory)
                if result["store"]:
                    decisions.append(self.add(user_id, result["content"], memory_type=result["memory_type"],
                        importance=result["importance"], confidence=result["confidence"],
                        source="conversation", conversation_id=conversation_id))
        memories = self.retrieve(user_id, message)
        prompt = self.builder.build_prompt(message, memories)
        result = {"stored_memories": decisions, "memories": memories, "stats": self.builder.get_stats(prompt)}
        if self.llm is None:
            result.update(response=None, generation_status="disabled")
        else:
            try:
                result.update(response=self.llm.generate(prompt), generation_status="ok")
            except Exception:
                result.update(response=None, generation_status="unavailable")
        return result

    def reflect(self, user_id):
        with self.lock:
            return ReflectionEngine(store=self.store).run(user_id)
