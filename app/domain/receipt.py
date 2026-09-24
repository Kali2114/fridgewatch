class ReceiptItem:
    def __init__(self, name: str, quantity: int) -> None:
        self.name = name
        self.quantity = quantity


class ReceiptParser:
    def __init__(self, client) -> None:
        self.client = client

    def parse(self, image_bytes):
        return [ReceiptItem(**item) for item in self.client.parse(image_bytes)]
