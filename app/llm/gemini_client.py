import json
import logging
from typing import Dict

# Import Google GenAI client
from google import genai

from app.config import get_settings

logger = logging.getLogger("email_composer")


class GeminiEmailGenerator:
    def __init__(self):
        settings = get_settings()

        # Configure using API key
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Use the Gemini 2.0 Flash model
        self.model_name = "gemini-2.5-flash"

    def _build_prompt(self, task: str, tone: str, constraints: str | None) -> str:
        return f"""
You are a professional email writing assistant.

Generate:
1. A concise email subject.
2. An HTML email body with clean, minimal inline styling.
3. A plain text fallback version.

Rules:
- Use simple inline CSS (e.g., font-family: Arial, line-height:1.6).
- Do not over-style the HTML.
- Respect the tone: {tone}.
- Fulfill the task: {task}.
- Additional constraints: {constraints or "None"}.

Return STRICT JSON (no markdown, no extra commentary):

{{
  "subject": "...",
  "html_body": "...",
  "text_body": "..."
}}
"""

    def generate_email(
        self,
        task: str,
        tone: str = "professional",
        constraints: str | None = None,
        max_retries: int = 2,
    ) -> Dict[str, str]:

        prompt = self._build_prompt(task, tone, constraints)

        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                raw_text = response.text.strip()

                # Strip out triple-backticks if any
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()

                parsed = json.loads(raw_text)

                # Validate keys
                if not all(k in parsed for k in ["subject", "html_body", "text_body"]):
                    raise ValueError("Gemini JSON missing required keys.")

                return parsed

            except Exception as e:
                logger.warning(
                    f"Gemini generation failed on attempt {attempt + 1}: {e}"
                )
                last_error = e

        # If all retries fail, raise the last exception
        raise RuntimeError(f"Failed to generate email content: {last_error}")
