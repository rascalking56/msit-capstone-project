import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import requests


class NotificationService:

    # -----------------------------
    # SMS via Twilio
    # -----------------------------
    @staticmethod
    def send_sms(to_number: str, message: str):
        client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH")
        )
        client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_FROM"),
            to=to_number
        )

    # -----------------------------
    # Email via SendGrid
    # -----------------------------
    @staticmethod
    def send_email(to_email: str, subject: str, message: str):
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        email = Mail(
            from_email=os.getenv("SENDGRID_FROM"),
            to_emails=to_email,
            subject=subject,
            html_content=message
        )
        sg.send(email)

    # -----------------------------
    # Outlook Email via Microsoft Graph
    # -----------------------------
    @staticmethod
    def send_outlook(to_email: str, subject: str, message: str):
        token = os.getenv("MS_GRAPH_TOKEN")

        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        payload = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": message},
                "toRecipients": [{"emailAddress": {"address": to_email}}],
            }
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        requests.post(url, json=payload, headers=headers)
