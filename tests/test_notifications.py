from app.notifications import build_reminder_email
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
