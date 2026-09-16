from app.domain.inventory import Item


def build_reminder_email(items: list[Item]) -> tuple[str, str]:
    subject = "Reminder email"
    names = [item.name for item in items]
    body = ", ".join(names)
    return subject, body
