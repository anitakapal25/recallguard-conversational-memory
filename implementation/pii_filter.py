"""
pii_filter.py

Detect and mask common PII before storing memories.
"""

import re


class PIIFilter:

    EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE = r"\b\d{10}\b"

    CREDIT_CARD = r"\b(?:\d[ -]*?){13,16}\b"

    AADHAR = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    PAN = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    def contains_pii(self, text: str) -> bool:

        patterns = [
            self.EMAIL,
            self.PHONE,
            self.CREDIT_CARD,
            self.AADHAR,
            self.PAN,
        ]

        return any(
            re.search(pattern, text)
            for pattern in patterns
        )

    def mask(self, text: str) -> str:

        text = re.sub(self.EMAIL, "[EMAIL]", text)
        text = re.sub(self.PHONE, "[PHONE]", text)
        text = re.sub(self.CREDIT_CARD, "[CARD]", text)
        text = re.sub(self.AADHAR, "[AADHAR]", text)
        text = re.sub(self.PAN, "[PAN]", text)

        return text

    def process(self, text: str):

        return {
            "contains_pii": self.contains_pii(text),
            "content": self.mask(text),
        }