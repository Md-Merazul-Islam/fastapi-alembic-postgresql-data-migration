import smtplib
from email.message import EmailMessage
import os


def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()  
    msg["From"] = os.getenv("MAIL_USERNAME")
    msg["To"] = to_email
    msg["Subject"] = "OTP Verification"
    msg.set_content(f"Your OTP is {otp}")

    with smtplib.SMTP(
        os.getenv("MAIL_SERVER"),
        int(os.getenv("MAIL_PORT"))  
    ) as server:
        server.starttls()
        server.login(
            os.getenv("MAIL_USERNAME"),
            os.getenv("MAIL_PASSWORD")
        )
        server.send_message(msg)