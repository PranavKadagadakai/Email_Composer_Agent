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

        # Define replacement values
        placeholder_values = {
            "recipient_name": request.to_email.split("@")[0],
            "sender_name": "Your Name",  # Replace dynamically if needed
        }

        # Apply rendering
        email_content["html_body"] = render_placeholders(
            email_content["html_body"], placeholder_values
        )

        email_content["text_body"] = render_placeholders(
            email_content["text_body"], placeholder_values
        )

        logger.info("Sending email via SMTP...")

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
