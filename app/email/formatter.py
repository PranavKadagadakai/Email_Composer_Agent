# app/email/formatter.py

import re
from typing import Dict

ALLOWED_PLACEHOLDERS = {
    "recipient_name",
    "sender_name",
    "company_name",
    "date",
}


def normalize_placeholders(content: str) -> str:
    """
    Normalizes common LLM placeholder variants to {{placeholder}} format.
    """

    patterns = {
        r"\[recipient_name\]": "{{recipient_name}}",
        r"\[sender_name\]": "{{sender_name}}",
        r"<recipient_name>": "{{recipient_name}}",
        r"<sender_name>": "{{sender_name}}",
    }

    for pattern, replacement in patterns.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    return content


def render_placeholders(content: str, values: Dict[str, str]) -> str:
    """
    Safely replaces allowed placeholders.
    Raises error if unknown placeholders remain.
    """

    content = normalize_placeholders(content)

    for key in ALLOWED_PLACEHOLDERS:
        placeholder = f"{{{{{key}}}}}"
        if placeholder in content:
            content = content.replace(placeholder, values.get(key, ""))

    # Detect unresolved placeholders
    unresolved = re.findall(r"\{\{.*?\}\}", content)
    if unresolved:
        raise ValueError(f"Unresolved placeholders detected: {unresolved}")

    return content
