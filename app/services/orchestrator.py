# app/services/orchestrator.py

import logging

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
