import logging
import smtplib
from email.message import EmailMessage

from app.config import get_settings

logger = logging.getLogger("email_composer")


class EmailSender:
    def __init__(self):
        self.settings = get_settings()

    def send(
        self,
        recipient: str,
        subject: str,
        html_body: str,
        text_body: str,
    ) -> bool:
        """
        Sends a multipart email (plain text + HTML) using SMTP.

        Raises exception on failure.
        """

        msg = EmailMessage()

        # Basic headers
        msg["Subject"] = subject
        msg["From"] = self.settings.SMTP_USER
        msg["To"] = recipient

        # Set plain text (fallback)
        msg.set_content(text_body)

        # Add HTML part
        msg.add_alternative(html_body, subtype="html")

        try:
            logger.info("Connecting to SMTP server...")

            with smtplib.SMTP(
                host=self.settings.SMTP_SERVER,
                port=self.settings.SMTP_PORT,
                timeout=10,
            ) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                logger.info("Logging in to SMTP...")
                smtp.login(
                    self.settings.SMTP_USER,
                    self.settings.SMTP_PASSWORD,
                )

                smtp.send_message(msg)
                logger.info(f"Email successfully sent to {recipient}.")
                logger.info(f"Email sent successfully with content {html_body}")

            return True

        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            raise
