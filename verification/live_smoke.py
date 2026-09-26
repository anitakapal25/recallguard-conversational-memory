"""Real MiniLM/Ollama/Flask smoke. Child process releases Windows DB locks before cleanup."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"implementation"),str(ROOT/".runtime"),str(ROOT)]


def run(path):
    import chromadb
    from chromadb.config import Settings
    from app import create_app
    from embeddings import SentenceEncoder
    from llm import LocalLLM
    from memory_store import MemoryStore
    from service import MemoryService
    encoder=SentenceEncoder()
    db=chromadb.PersistentClient(path=path,settings=Settings(anonymized_telemetry=False))
    store=MemoryStore(collection=db.create_collection("live_smoke",embedding_function=None))
    service=MemoryService(store,encoder,LocalLLM())
    client=create_app(service,{"smoke-key":"synthetic-user"}).test_client()
    headers={"X-API-Key":"smoke-key"}
    initial=client.post("/memory",headers=headers,json={"text":"I prefer Python for programming.","memory_type":"preference","consent":True})
    assert initial.status_code==201,initial.json
    response=client.post("/chat",headers=headers,json={"message":"Which programming language do I prefer?"})
    assert response.status_code==200,response.json
    assert response.json["generation_status"]=="ok"
    assert "python" in response.json["response"].lower(),response.json
    mid=initial.json["memory_id"]
    assert client.put("/memory/"+mid,headers=headers,json={"text":"I prefer Rust for programming.","consent":True}).status_code==200
    result=client.post("/chat",headers=headers,json={"message":"Which programming language do I prefer?"})
    assert result.status_code==200,result.json
    assert "rust" in result.json["response"].lower(),result.json
    assert client.delete("/memory/"+mid,headers=headers).status_code==200
    assert client.get("/memory/"+mid,headers=headers).status_code==404
    report={"status":"passed","scope":"One synthetic live scenario; not a broad response-quality benchmark",
            "model":service.llm.model,"initial_response":response.json["response"],"corrected_response":result.json["response"]}
    (ROOT/"verification/results/live-smoke.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--database")
    args=parser.parse_args()
    if args.database:
        run(args.database)
    else:
        with tempfile.TemporaryDirectory(prefix="recallguard-live-") as path:
            subprocess.run([sys.executable,__file__,"--database",path],check=True)
