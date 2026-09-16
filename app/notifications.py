import smtplib
from email.message import EmailMessage

from app.config import settings
from app.domain.inventory import Item


def build_reminder_email(items: list[Item]) -> tuple[str, str]:
    subject = "Reminder email"
    names = [item.name for item in items]
    body = ", ".join(names)
    return subject, body


def send_reminder_email(to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to
    msg.set_content(body)
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(
            settings.smtp_user,
            settings.smtp_password,
        )
        server.send_message(msg)
