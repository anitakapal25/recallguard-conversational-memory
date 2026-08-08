"""
auth.py

Authentication and authorization module
for the Conversational Memory System.
"""

import hashlib
import secrets
from functools import wraps
from typing import Dict

from flask import jsonify, request


class AuthManager:

    def __init__(self):

        # In production this should come from
        # a secure database or secrets manager.

        self.users: Dict = {
            "admin-key": {
                "user_id": "admin",
                "role": "admin",
            },
            "user-key": {
                "user_id": "user_1",
                "role": "user",
            },
        }

    # --------------------------------------------------
    # API Key Validation
    # --------------------------------------------------

    def authenticate(
        self,
        api_key: str,
    ):

        return self.users.get(api_key)

    # --------------------------------------------------
    # Get Current User
    # --------------------------------------------------

    def current_user(self):

        api_key = request.headers.get(
            "X-API-Key"
        )

        if not api_key:
            return None

        return self.authenticate(api_key)

    # --------------------------------------------------
    # Generate API Key
    # --------------------------------------------------

    def generate_api_key(self):

        return secrets.token_hex(32)

    # --------------------------------------------------
    # Hash Sensitive Values
    # --------------------------------------------------

    @staticmethod
    def hash_value(value: str):

        return hashlib.sha256(
            value.encode()
        ).hexdigest()


auth_manager = AuthManager()


# ======================================================
# Authentication Decorator
# ======================================================

def login_required(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        user = auth_manager.current_user()

        if user is None:

            return (
                jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ),
                401,
            )

        request.user = user

        return func(
            *args,
            **kwargs,
        )

    return wrapper


# ======================================================
# Admin Decorator
# ======================================================

def admin_required(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        user = auth_manager.current_user()

        if user is None:

            return (
                jsonify(
                    {
                        "error": "Unauthorized"
                    }
                ),
                401,
            )

        if user["role"] != "admin":

            return (
                jsonify(
                    {
                        "error": "Forbidden"
                    }
                ),
                403,
            )

        request.user = user

        return func(
            *args,
            **kwargs,
        )

    return wrapper