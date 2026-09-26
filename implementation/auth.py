"""Fail-closed, per-app API-key authentication configured outside source."""
import json
import os
import secrets
from functools import wraps
from flask import current_app, g, jsonify, request


class AuthManager:
    def __init__(self, users=None):
        self.users = users if users is not None else json.loads(os.environ.get("RECALLGUARD_API_KEYS", "{}"))
        if not isinstance(self.users, dict) or any(
            not isinstance(key, str) or not key or not isinstance(value, str) or not value
            for key, value in self.users.items()
        ):
            raise ValueError("RECALLGUARD_API_KEYS must map nonempty API keys to nonempty user IDs")

    def authenticate(self, key):
        for configured, user_id in self.users.items():
            if secrets.compare_digest(configured.encode("utf-8"), key.encode("utf-8")):
                return {"user_id": user_id}
        return None


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key", "")
        user = current_app.extensions["auth"].authenticate(key)
        if user is None:
            return jsonify(error="Unauthorized"), 401
        g.user_id = user["user_id"]
        return func(*args, **kwargs)
    return wrapper
