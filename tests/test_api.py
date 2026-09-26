import pytest

A = {"X-API-Key": "test-a"}
B = {"X-API-Key": "test-b"}


def add(client, text="I prefer coffee"):
    response = client.post("/memory", headers=A, json={"text": text, "consent": True})
    assert response.status_code == 201
    return response.json["memory_id"]


def test_end_to_end_restart_session_correction_delete(client):
    mid = add(client)
    assert client.get("/memory/" + mid, headers=A).status_code == 200
    result = client.post("/retrieve", headers=A, json={"query": "coffee"})
    assert result.status_code == 200 and result.json[0]["id"] == mid
    result = client.put("/memory/" + mid, headers=A, json={"text": "I prefer tea", "consent": True})
    assert result.status_code == 200
    assert client.get("/memory/" + mid, headers=A).json["documents"] == ["I prefer tea"]
    assert client.delete("/memory/" + mid, headers=A).status_code == 200
    assert client.get("/memory/" + mid, headers=A).status_code == 404


@pytest.mark.parametrize("method", ["get", "delete", "put"])
def test_cross_owner_object_access(client, method):
    mid = add(client)
    kwargs = {"headers": B}
    if method == "put":
        kwargs["json"] = {"text": "I prefer tea", "consent": True}
    assert getattr(client, method)("/memory/" + mid, **kwargs).status_code == 404
    assert client.get("/memory/" + mid, headers=A).status_code == 200


def test_authentication_required(client):
    assert client.get("/memories").status_code == 401
    assert client.get("/memories", headers={"X-API-Key": "user-key"}).status_code == 401
    assert client.get("/memories", headers={"X-API-Key": "caf\u00e9"}).status_code == 401


@pytest.mark.parametrize("payload", [
    [], {"text": 12, "consent": True}, {"text": "ok", "consent": False},
    {"text": "valid", "consent": True, "importance": "bad"},
    {"text": "valid", "consent": True, "confidence": float("nan")},
    {"text": "valid", "consent": True, "memory_type": "unknown"},
    {"text": "valid", "consent": True, "retention_days": 100},
])
def test_invalid_store_input(client, payload):
    assert client.post("/memory", headers=A, json=payload).status_code == 400


@pytest.mark.parametrize("value", [0, -1, 21, True, "5"])
def test_invalid_top_k(client, value):
    assert client.post("/retrieve", headers=A, json={"query": "coffee", "top_k": value}).status_code == 400


def test_sensitive_write_and_update_blocked(client):
    mid = add(client)
    for path, method in [("/memory", "post"), ("/memory/" + mid, "put")]:
        result = getattr(client, method)(path, headers=A, json={"text": "My password is secret", "consent": True})
        assert result.status_code == 400
    assert client.get("/memory/" + mid, headers=A).json["documents"] == ["I prefer coffee"]


def test_errors_and_logs_do_not_expose_content(client, service, caplog):
    class BrokenStore:
        def list_memories(self, user):
            raise RuntimeError("PRIVATE-MEMORY-CONTENT")
    service.store = BrokenStore()
    response = client.get("/memories", headers=A)
    assert response.status_code == 503
    assert "PRIVATE-MEMORY-CONTENT" not in response.text + caplog.text
    assert response.headers["X-Request-ID"]


def test_generation_failure_is_explicit(client, service):
    class Failed:
        def generate(self, prompt):
            raise RuntimeError("private")
    service.llm = Failed()
    result = client.post("/chat", headers=A, json={"message": "I like coffee", "remember": True})
    assert result.status_code == 503
    assert result.json["stored_memories"][0]["status"] == "stored"


def test_input_limit_and_safe_headers(client):
    assert client.post("/memory", headers=A, data="x" * 70000, content_type="application/json").status_code == 413
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]


def test_cross_owner_search_and_reflection(client):
    add(client)
    assert client.get("/memories", headers=B).json["ids"] == []
    assert client.post("/retrieve", headers=B, json={"query": "coffee"}).json == []
    assert client.post("/reflection", headers=B).json["summary"]["total"] == 0
    assert len(client.get("/memories", headers=A).json["ids"]) == 1
