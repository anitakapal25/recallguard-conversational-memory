"""Run the real app on loopback with a persistent, isolated local test profile."""
import json
import os
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "implementation"), str(ROOT / ".runtime")]

if __name__ == "__main__":
    state = ROOT / "tmp" / "local-app"
    state.mkdir(parents=True, exist_ok=True)
    key_file = state / "api-key.txt"
    if not key_file.exists():
        key_file.write_text(secrets.token_urlsafe(32), encoding="utf-8")
    os.environ["RECALLGUARD_API_KEYS"] = json.dumps({key_file.read_text().strip(): "local-tester"})
    os.environ["RECALLGUARD_DB_PATH"] = str(state / "chroma")
    os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
    os.environ["RECALLGUARD_LLM_MODEL"] = "llama3.2:3b"
    from app import create_app
    from waitress import serve
    app = create_app()
    print("RecallGuard: http://127.0.0.1:5000 | key: tmp/local-app/api-key.txt", flush=True)
    serve(app, host="127.0.0.1", port=5000, threads=4)
