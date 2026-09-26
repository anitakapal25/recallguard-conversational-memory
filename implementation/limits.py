"""Bounded per-owner limits for the single-process free demo deployment."""
from collections import deque
from threading import Lock
from time import monotonic


class DemoLimits:
    def __init__(self, clock=monotonic):
        self.clock, self.lock, self.windows = clock, Lock(), {}

    def allow(self, owner, generation=False):
        with self.lock:
            now = self.clock()
            buckets = [(owner, "requests", 60, 60)]
            if generation:
                buckets += [(owner, "generation", 60, 5), ("global", "daily-generation", 86400, 200)]
            queues = []
            for who, kind, seconds, limit in buckets:
                queue = self.windows.setdefault((who, kind), deque())
                while queue and queue[0] <= now-seconds:
                    queue.popleft()
                if len(queue) >= limit:
                    return False
                queues.append(queue)
            for queue in queues:
                queue.append(now)
            return True


def install_limits(app):
    from flask import request, jsonify
    limiter = DemoLimits()
    @app.before_request
    def limit_cloud_requests():
        if request.endpoint in {"home", "health", "ready", "static"}:
            return None
        user = app.extensions["auth"].authenticate(request.headers.get("X-API-Key", ""))
        if user is None:
            return jsonify(error="Unauthorized"), 401
        if not limiter.allow(user["user_id"], request.endpoint == "chat"):
            return jsonify(error="Demo request limit reached. Try later."), 429
