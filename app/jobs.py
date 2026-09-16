from app.domain.inventory import items_expiring_soon
from app.notifications import build_reminder_email, send_reminder_email


def run_reminder_job(item_repository, user_repository, today) -> None:
    items = item_repository.list_all()
    expiring_items = items_expiring_soon(items, today)
    groups = {}
    for item in expiring_items:
        groups.setdefault(item.user_id, []).append(item)
    for user_id, user_items in groups.items():
        user = user_repository.get_user(user_id)
        subject, body = build_reminder_email(user_items)
        send_reminder_email(user.email, subject, body)
