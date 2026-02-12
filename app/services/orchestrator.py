# app/services/orchestrator.py

import logging

from app.email.formatter import render_placeholders
from app.email.sender import EmailSender
from app.llm.gemini_client import GeminiEmailGenerator
from app.schemas import EmailRequest

logger = logging.getLogger("email_composer")


class EmailOrchestrator:
    def __init__(self):
        self.generator = GeminiEmailGenerator()
        self.sender = EmailSender()

    def compose_and_send(self, request: EmailRequest) -> dict:
        logger.info("Generating email content via Gemini...")

        email_content = self.generator.generate_email(
            task=request.task,
            tone=request.tone,
            constraints=request.constraints,
        )

        # --------------------------
        # Name Resolution (LLM-driven)
        # --------------------------

        recipient_fallback = request.to_email.split("@")[0]

        recipient_name = email_content.get("recipient_name") or recipient_fallback

        sender_name = (
            getattr(request, "sender_name", None)
            or email_content.get("sender_name")
            or recipient_fallback
        )

        placeholder_values = {
            "recipient_name": recipient_name,
            "sender_name": sender_name,
        }

        # Replace placeholders deterministically
        email_content["html_body"] = render_placeholders(
            email_content["html_body"],
            placeholder_values,
        )

        email_content["text_body"] = render_placeholders(
            email_content["text_body"],
            placeholder_values,
        )

        self.sender.send(
            recipient=request.to_email,
            subject=email_content["subject"],
            html_body=email_content["html_body"],
            text_body=email_content["text_body"],
        )

        return {
            "status": "sent",
            "subject": email_content["subject"],
            "recipient": request.to_email,
        }
