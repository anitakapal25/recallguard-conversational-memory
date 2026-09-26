"""Run separately: python implementation/maintenance.py [--once] [--interval 3600]."""
import argparse
import time
from memory_store import MemoryStore
from reflection import ReflectionEngine


def sweep(store):
    users = {m["user_id"] for m in store.collection.get(include=["metadatas"])["metadatas"]}
    return [ReflectionEngine(store=store).run(user) for user in sorted(users)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=3600)
    args = parser.parse_args()
    if args.interval < 1:
        parser.error("--interval must be positive")
    store = MemoryStore()
    while True:
        results = sweep(store)
        print({"users_processed": len(results), "expired": sum(r["maintenance"]["expired"] for r in results)})
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
