from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_post_recipe(recipe_fresh_repository):
    payload = {
        "name": "test_name",
        "required_ingredients": ["test_ingredient"],
    }
    res = client.post("/recipes", json=payload)

    assert res.status_code == 201
    assert res.json() == {
        "id": 1,
        "name": "test_name",
        "required_ingredients": ["test_ingredient"],
    }
