import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))


def send_reset_email(to_email: str, reset_code: str) -> bool:
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        return False

    message = EmailMessage()
    message["Subject"] = "ShopEase Password Reset"
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message.set_content(
        f"""Hello,

You requested to reset your ShopEase password.

Your password reset code is: {reset_code}

This code will expire in 10 minutes.

Regards,
ShopEase Team
"""
    )

    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.send_message(message)

    return True
