"""Single-process host entry point; provider secrets come from the environment."""
import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"implementation"))
from app import create_app
from waitress import serve

if __name__ == "__main__":
    if os.environ.get("RECALLGUARD_RUNTIME") != "cloud":
        raise RuntimeError("Cloud runtime must be explicitly configured")
    if not os.environ.get("RECALLGUARD_API_KEYS"):
        raise RuntimeError("An API key map is required")
    serve(create_app(),host="0.0.0.0",port=int(os.environ.get("PORT","10000")),threads=2)
