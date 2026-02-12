# app/email/formatter.py

import re
from typing import Dict

PLACEHOLDER_KEYS = {
    "recipient_name",
    "sender_name",
}


def normalize_placeholders(content: str) -> str:
    """
    Convert common LLM placeholder variations into {{key}} format.
    Handles:
        {recipient_name}
        {{recipient_name}}
        [recipient_name]
        <recipient_name>
        recipient_name
    """

    for key in PLACEHOLDER_KEYS:
        patterns = [
            rf"\{{\{{\s*{key}\s*\}}\}}",  # {{ key }}
            rf"\{{\s*{key}\s*\}}",  # { key }
            rf"\[\s*{key}\s*\]",  # [ key ]
            rf"<\s*{key}\s*>",  # < key >
        ]

        for pattern in patterns:
            content = re.sub(
                pattern,
                f"{{{{{key}}}}}",
                content,
                flags=re.IGNORECASE,
            )

    return content


def render_placeholders(content: str, values: Dict[str, str]) -> str:
    content = normalize_placeholders(content)

    for key, value in values.items():
        placeholder = f"{{{{{key}}}}}"
        content = content.replace(placeholder, value)

    # Detect unresolved placeholders
    unresolved = re.findall(r"\{\{.*?\}\}", content)
    if unresolved:
        raise ValueError(f"Unresolved placeholders detected: {unresolved}")

    return content
