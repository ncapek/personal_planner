"""
This module provides functionality to send emails using the SendGrid service.

It uses the SendGrid API to send an HTML email from a specified sender to a specified recipient.
The module reads the necessary configuration from environment variables for security and convenience,
allowing the API key, sender email, recipient email, and subject to be set without hardcoding
values into the source code.

The main function `send_email` can be imported and used in other modules, or this script can be
run directly to send an email with predefined content.

Usage:
    Set environment variables for SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL, and SUBJECT.
    Run the script directly or import the send_email function in another module to send an email.

"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import NoReturn
from config import SENDGRID_API_KEY, FROM_EMAIL, TO_EMAIL, SUBJECT
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(from_email: str, to_email: str, subject: str, html_content: str) -> NoReturn:
    """
    Sends an email using the SendGrid API.

    Args:
        from_email (str): The email address of the sender.
        to_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        html_content (str): The HTML content of the email.

    Returns:
        NoReturn: This function does not return anything.
    """
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent with status code: {response.status_code}")
        logger.info("Morning briefing successfully sent by email.")
    except Exception as e:
        logger.error(f"An error occurred while sending the email: {e}")

# Usage example:
if __name__ == "__main__":
    html_content = '<strong>This is a test.</strong>'
    send_email(FROM_EMAIL, TO_EMAIL, SUBJECT, html_content)
