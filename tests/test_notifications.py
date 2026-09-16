from unittest.mock import patch

from app.config import settings
from app.notifications import build_reminder_email, send_reminder_email
from tests.domain.utils import create_item


def test_reminder_email():
    item1 = create_item(name="test_item1")
    item2 = create_item(name="test_item2")
    result = build_reminder_email([item1, item2])
    subject, body = result

    assert isinstance(subject, str)
    assert isinstance(body, str)
    assert "test_item1" in body
    assert "test_item2" in body


def test_send_email():
    with patch("app.notifications.smtplib.SMTP") as mock_smtp:
        send_reminder_email(
            to="test@example.com",
            subject="Reminder",
            body="Milk expires soon",
        )

        server = mock_smtp.return_value.__enter__.return_value
        server.starttls.assert_called_once()
        server.login.assert_called_once_with(
            settings.smtp_user,
            settings.smtp_password,
        )
        server.send_message.assert_called_once()
