from app.domain.receipt import ReceiptItem, ReceiptParser
from tests.domain.utils import create_receipt_item


class FakeReceiptClient:

    def parse(self, image_bytes):
        return [{"name": "test", "quantity": 2}]


class TestReceipt:
    def test_create_receipt_item(self):
        receipt = create_receipt_item(name="test", quantity=2)

        assert receipt.name == "test"
        assert receipt.quantity == 2

    def test_receipt_item_parser(self):
        image_bytes = b"fake receipt image"
        client = FakeReceiptClient()
        parser = ReceiptParser(client)
        result = parser.parse(image_bytes)

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], ReceiptItem)
        assert result[0].name == "test"
        assert result[0].quantity == 2
