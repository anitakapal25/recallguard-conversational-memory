"""Flask app factory. Production invocation: waitress-serve --call app:create_app."""
import time
import uuid
from flask import Flask, g, jsonify, render_template, request
from werkzeug.exceptions import HTTPException
from auth import AuthManager, login_required


def create_app(service=None, api_keys=None):
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024
    app.extensions["auth"] = AuthManager(api_keys)
    if service is None:
        from embeddings import SentenceEncoder
        from llm import LocalLLM
        from memory_store import MemoryStore
        from service import MemoryService
        service = MemoryService(MemoryStore(), SentenceEncoder(), LocalLLM())
    app.extensions["memory_service"] = service

    @app.before_request
    def begin():
        g.request_id = str(uuid.uuid4())
        g.started = time.perf_counter()

    @app.after_request
    def finish(response):
        response.headers["X-Request-ID"] = g.request_id
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'"
        app.logger.info("request id=%s method=%s status=%s duration_ms=%.2f",
                        g.request_id, request.method, response.status_code, (time.perf_counter()-g.started)*1000)
        return response

    @app.errorhandler(ValueError)
    def invalid(error):
        return jsonify(error=str(error), request_id=g.request_id), 400

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.name, request_id=g.request_id), error.code

    @app.errorhandler(Exception)
    def unavailable(error):
        # Never expose or log raw provider exceptions, prompts or database documents.
        app.logger.error("operation_failed request_id=%s exception_type=%s", g.request_id, type(error).__name__)
        return jsonify(error="Service unavailable", request_id=g.request_id), 503

    def body():
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError("JSON object required")
        return data

    @app.get("/")
    def home():
        return render_template("chat.html")

    @app.get("/health")
    def health():
        return jsonify(status="alive")

    @app.get("/ready")
    def ready():
        service.store.collection.count()
        return jsonify(storage="ready", generation="not_checked")

    @app.get("/memories")
    @login_required
    def memories():
        return jsonify(service.store.list_memories(g.user_id))

    @app.post("/memory")
    @login_required
    def add():
        data = body()
        if data.get("consent") is not True:
            raise ValueError("consent=true is required to store memory")
        result = service.add(g.user_id, data.get("text"), memory_type=data.get("memory_type", "conversation"),
                             importance=data.get("importance", 0.5), confidence=data.get("confidence", 0.9),
                             retention_days=data.get("retention_days", 7))
        return jsonify(result), 201 if result["status"] == "stored" else 200

    @app.get("/memory/<mid>")
    @login_required
    def get(mid):
        result = service.store.get_memory(mid, g.user_id)
        return (jsonify(result), 200) if result["ids"] else (jsonify(error="Memory not found"), 404)

    @app.put("/memory/<mid>")
    @login_required
    def update(mid):
        data = body()
        if data.get("consent") is not True:
            raise ValueError("consent=true is required")
        if not service.correct(g.user_id, mid, data.get("text")):
            return jsonify(error="Memory not found"), 404
        return jsonify(status="corrected", memory_id=mid)

    @app.delete("/memory/<mid>")
    @login_required
    def delete(mid):
        with service.lock:
            deleted = service.store.delete_memory(mid, g.user_id)
        return (jsonify(status="deleted"), 200) if deleted else (jsonify(error="Memory not found"), 404)

    @app.post("/retrieve")
    @login_required
    def retrieve():
        data = body()
        return jsonify(service.retrieve(g.user_id, data.get("query"), data.get("top_k", 5)))

    @app.post("/context")
    @login_required
    def context():
        data = body()
        query = service.safe_text(data.get("query"))
        ranked = service.retrieve(g.user_id, query)
        prompt = service.builder.build_prompt(query, ranked)
        return jsonify(prompt=prompt, stats=service.builder.get_stats(prompt))

    @app.post("/chat")
    @login_required
    def chat():
        data = body()
        remember = data.get("remember", False)
        if not isinstance(remember, bool):
            raise ValueError("remember must be boolean")
        conversation_id = data.get("conversation_id", "")
        if not isinstance(conversation_id, str) or len(conversation_id) > 128:
            raise ValueError("conversation_id must be a string of at most 128 characters")
        if service.pii.contains_pii(conversation_id):
            raise ValueError("conversation_id must not contain sensitive content")
        result = service.chat(g.user_id, data.get("message"), remember, conversation_id)
        result["request_id"] = g.request_id
        return jsonify(result), 503 if result["generation_status"] == "unavailable" else 200

    @app.post("/reflection")
    @login_required
    def reflection():
        return jsonify(service.reflect(g.user_id))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
