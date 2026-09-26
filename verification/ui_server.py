"""Loopback-only synthetic UI test harness. Never use these keys for deployment."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"implementation"),str(ROOT/".runtime"),str(ROOT)]
from waitress import serve
from app import create_app
from memory_store import MemoryStore
from service import MemoryService
from verification.support import HashEncoder


class DemonstrationLLM:
    def generate(self,prompt):
        return "UI test response (deterministic test double). Inspect retrieved memories below."


with tempfile.TemporaryDirectory(prefix="recallguard-ui-",ignore_cleanup_errors=True) as path:
    service=MemoryService(MemoryStore(path=path),HashEncoder(),DemonstrationLLM())
    app=create_app(service,{"ui-smoke-only":"ui-user"})
    serve(app,host="127.0.0.1",port=5055,threads=4)
