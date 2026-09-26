import pytest
from limits import DemoLimits
from cloud import SupabaseCollection, GroqLLM


class Transport:
    def __init__(self, result=None, ok=True):
        self.result, self.ok, self.calls = result, ok, []
    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self
    def json(self):
        return self.result


def test_storage_owner_required_before_network():
    transport = Transport([])
    store = SupabaseCollection("https://example.supabase.co", "secret", transport)
    with pytest.raises(ValueError):
        store.get(ids=["foreign"])
    with pytest.raises(ValueError):
        store.delete(["foreign"], {})
    assert transport.calls == []


def test_query_preserves_owner_active_ids_and_squared_distance():
    transport = Transport([{"id":"one","document":"coffee","metadata":{"user_id":"alice"},"distance":0.5}])
    store = SupabaseCollection("https://example.supabase.co", "secret", transport)
    result = store.query([[1,0]],5,["one"],{"user_id":"alice"})
    assert result["ids"] == [["one"]]
    assert result["distances"] == [[0.5]]
    payload = transport.calls[0][1]["json"]
    assert payload["p_owner"] == "alice" and payload["p_ids"] == ["one"]


def test_update_never_drops_owner():
    transport = Transport(True)
    store = SupabaseCollection("https://example.supabase.co", "secret", transport)
    store.update(["one"],["tea"],[[1]], [{"user_id":"alice"}])
    assert transport.calls[0][1]["json"]["p_owner"] == "alice"
    assert transport.calls[0][1]["json"]["p_update"] is True


def test_provider_error_does_not_include_secrets():
    transport = Transport({"error":"secret provider details"},ok=False)
    for action in [lambda: SupabaseCollection("https://example.supabase.co","secret",transport).count(),
                   lambda: GroqLLM("secret",transport).generate("private message")]:
        with pytest.raises(RuntimeError) as error:
            action()
        assert "secret" not in str(error.value)
        assert "private" not in str(error.value)


def test_groq_output_bounded_and_system_separate():
    transport = Transport({"choices":[{"message":{"content":"Hello"}}]})
    assert GroqLLM("secret",transport).generate("data") == "Hello"
    payload = transport.calls[0][1]["json"]
    assert payload["max_completion_tokens"] == 128
    assert payload["messages"][0]["role"] == "system"
    assert transport.calls[0][1]["timeout"] == 30


def test_limits_owner_separation_and_window_recovery():
    now = [0]
    limits = DemoLimits(lambda: now[0])
    assert all(limits.allow("alice",True) for _ in range(5))
    assert not limits.allow("alice",True)
    assert limits.allow("bob",True)
    assert limits.allow("alice",False)
    now[0] = 60
    assert limits.allow("alice",True)


def test_cloud_limit_returns_429_without_breaking_request_headers(client, monkeypatch):
    from app import create_app
    monkeypatch.setenv("RECALLGUARD_RUNTIME","cloud")
    app = create_app(client.application.extensions["memory_service"],{"key":"alice"})
    test = app.test_client()
    for _ in range(60):
        assert test.get("/memories",headers={"X-API-Key":"key"}).status_code == 200
    result = test.get("/memories",headers={"X-API-Key":"key"})
    assert result.status_code == 429
    assert result.headers["X-Request-ID"]
