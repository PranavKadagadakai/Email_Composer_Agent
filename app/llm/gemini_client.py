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
    You are a deterministic email generation engine.

    Your task is to generate a COMPLETE email based ONLY on the given task.

    Do NOT:
    - Ask for more information.
    - Provide instructions.
    - Provide guidance.
    - Add assistant-style conversational text.
    - Add welcome messages.
    - Add meta commentary.
    - Add explanation.

    You MUST:
    - Extract recipient name if explicitly mentioned.
    - Extract sender name if explicitly mentioned.
    - If not mentioned, return null for that field.
    - Use ONLY these placeholders in the email body:
      {{recipient_name}}
      {{sender_name}}

    Generate:
    1. subject
    2. html_body
    3. text_body
    4. recipient_name (string or null)
    5. sender_name (string or null)

    The email must be fully written and complete.
    It must NOT ask the user for additional information.

    Tone: {tone}
    Task: {task}
    Additional constraints: {constraints or "None"}

    Return STRICT JSON ONLY.
    No markdown.
    No explanation.
    No extra text.

    Expected format:

    {{
      "subject": "...",
      "html_body": "...",
      "text_body": "...",
      "recipient_name": "Name or null",
      "sender_name": "Name or null"
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
                required_keys = [
                    "subject",
                    "html_body",
                    "text_body",
                    "recipient_name",
                    "sender_name",
                ]

                if not all(k in parsed for k in required_keys):
                    raise ValueError("Invalid JSON structure from Gemini.")

                return parsed

            except Exception as e:
                logger.warning(
                    f"Gemini generation failed on attempt {attempt + 1}: {e}"
                )
                last_error = e

        # If all retries fail, raise the last exception
        raise RuntimeError(f"Failed to generate email content: {last_error}")
