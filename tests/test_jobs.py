from datetime import date, timedelta
from unittest.mock import patch

from app.domain.repository import InMemoryItemRepository
from app.domain.user_repository import InMemoryUserRepository
from app.jobs import run_reminder_job
from app.notifications import build_reminder_email
from tests.domain.utils import create_item, create_user


def test_reminder_job_sends_email():
    item_repository = InMemoryItemRepository()
    user_repository = InMemoryUserRepository()
    user = create_user()
    user_repository.add_user(user)
    item = create_item()
    item2 = create_item(
        name="test_item2", expiry_date=date.today() + timedelta(days=10)
    )
    item_repository.add_item(item)
    item_repository.add_item(item2)
    with patch("app.jobs.send_reminder_email") as mock_send:
        run_reminder_job(
            item_repository,
            user_repository,
            date.today(),
        )
        subject, body = build_reminder_email([item])
        mock_send.assert_called_once_with(user.email, subject, body)
