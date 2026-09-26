"""Deterministic lexical embeddings for offline contract checks, NOT semantic evidence."""
import hashlib
import math
import re


class HashEncoder:
    name = "sha256-word-buckets-256 (lexical test double)"

    def encode(self, text):
        vector = [0.0] * 256
        for token in re.findall(r"\w+", text.casefold()):
            index = int.from_bytes(hashlib.sha256(token.encode()).digest()[:4], "big") % len(vector)
            vector[index] += 1
        norm = math.sqrt(sum(x*x for x in vector)) or 1
        return [x / norm for x in vector]
