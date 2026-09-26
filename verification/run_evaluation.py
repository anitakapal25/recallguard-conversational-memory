"""python verification/run_evaluation.py [--semantic]. Uses a temporary database only."""
import argparse
import csv
import hashlib
import json
import platform
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "implementation"), str(ROOT)]
import chromadb
from chromadb.config import Settings
from memory_store import MemoryStore
from service import MemoryService
from context_builder import ContextBuilder
from verification.support import HashEncoder
from experiments.naive_baseline.baseline import NaiveBaseline


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[round((len(ordered)-1)*fraction)]


def evaluate(encoder, dataset, output):
    rows, errors = [], []
    with tempfile.TemporaryDirectory(prefix="recallguard-eval-") as directory:
        client = chromadb.PersistentClient(path=directory, settings=Settings(anonymized_telemetry=False))
        for case in dataset:
            for mode in ["baseline", "improved"]:
                collection = client.create_collection(case["id"] + "-" + mode, embedding_function=None)
                now = [datetime(2026, 9, 25, tzinfo=timezone.utc)]
                store = MemoryStore(collection=collection, clock=lambda: now[0])
                system = MemoryService(store, encoder) if mode == "improved" else NaiveBaseline(collection, encoder)
                ids, labels = {}, {}
                for entry in case["memories"]:
                    label,user,text,*extra = entry
                    if mode == "baseline":
                        mid = system.add(user,text)
                    else:
                        try:
                            mid = system.add(user,text,confidence=extra[0] if extra else .9,
                                             source="evaluation",conversation_id=case["id"])["memory_id"]
                        except ValueError:
                            continue
                    ids[label] = mid
                    labels.setdefault(mid,label)
                for op in case.get("operations",[]):
                    if op["action"] == "advance":
                        now[0] += timedelta(days=op["days"])
                    elif op["action"] == "correct":
                        if mode == "baseline":
                            mid = system.add("alice",op["text"])
                            labels[mid] = op["id"] + "-new"
                        else:
                            system.correct("alice",ids[op["id"]],op["text"])
                    elif op["action"] == "delete" and mode == "improved":
                        store.delete_memory(ids[op["id"]],"alice")
                durations = []
                for _ in range(7):
                    start = time.perf_counter()
                    result = system.retrieve("alice",case["query"],case.get("top_k",5))
                    durations.append((time.perf_counter()-start)*1000)
                actual = [labels[r["id"]] for r in result]
                expected = set(case["expected"])
                hits = len(expected.intersection(actual))
                precision = hits/len(actual) if actual else (1.0 if not expected else 0.0)
                recall = hits/len(expected) if expected else (1.0 if not actual else 0.0)
                stale = any(fragment in r["content"] for fragment in case.get("forbidden_text",[]) for r in result)
                leak = any(r["metadata"]["user_id"] != "alice" for r in result)
                prompt = (system.builder.build_prompt(case["query"],result) if mode == "improved"
                          else ContextBuilder._render(case["query"],result))
                prompt_units = len(prompt.encode("utf-8"))
                budget_ok = prompt_units + 128 + 160 <= 1000
                passed = set(actual) == expected and not stale and not leak and (budget_ok or not case.get("budget_check"))
                documents = collection.get()["documents"]
                row = {"case":case["id"],"mode":mode,"precision_at_k":precision,"recall_at_k":recall,
                       "p50_ms":percentile(durations,.5),"p95_ms":percentile(durations,.95),
                       "first_query_ms":durations[0],"stored_records":collection.count(),
                       "stored_content_bytes":sum(len(d.encode("utf-8")) for d in documents),
                       "prompt_utf8_units":prompt_units,"budget_ok":budget_ok,"stale_or_sensitive":stale,
                       "cross_user_leak":leak,"passed":passed,"actual":"|".join(actual)}
                rows.append(row)
                if not passed:
                    errors.append({"case":case["id"],"mode":mode,"expected":case["expected"],"actual":actual,
                                   "stale_or_sensitive":stale,"budget_ok":budget_ok})
                client.delete_collection(collection.name)
        # Stop connections before TemporaryDirectory cleanup on Windows.
        client._system.stop()
    output.mkdir(parents=True,exist_ok=True)
    with (output/"comparison.csv").open("w",newline="",encoding="utf-8") as stream:
        writer = csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (output/"error_examples.jsonl").write_text("".join(json.dumps(e)+"\n" for e in errors),encoding="utf-8")
    summary = {"generated_at":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),
               "chromadb":version("chromadb"),"encoder":getattr(encoder,"name","all-MiniLM-L6-v2"),
               "dataset_sha256":hashlib.sha256((ROOT/"verification/evaluation_dataset.jsonl").read_bytes()).hexdigest(),
               "scope":"Offline retrieval/policy benchmark. No generated-response quality or model-token measurement.",
               "latency_scope":"7 retrieval calls per case, first call included; no LLM or model startup time.",
               "results":{}}
    for mode in ["baseline","improved"]:
        group=[r for r in rows if r["mode"]==mode]
        summary["results"][mode]={"passed":sum(r["passed"] for r in group),"total":len(group),
            "mean_precision_at_k":sum(r["precision_at_k"] for r in group)/len(group),
            "mean_recall_at_k":sum(r["recall_at_k"] for r in group)/len(group)}
    (output/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return summary


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--semantic",action="store_true")
    args=parser.parse_args()
    if args.semantic:
        from embeddings import SentenceEncoder
        encoder=SentenceEncoder()
    else:
        encoder=HashEncoder()
    dataset=[json.loads(line) for line in (ROOT/"verification/evaluation_dataset.jsonl").read_text(encoding="utf-8").splitlines()]
    evaluate(encoder,dataset,ROOT/"verification/results"/("semantic" if args.semantic else "offline"))
