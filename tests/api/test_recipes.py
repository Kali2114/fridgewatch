from fastapi.testclient import TestClient

from app.domain.recipe import Recipe
from app.main import app
from tests.domain import utils
from tests.domain.utils import create_recipe

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


def test_list_recipes(recipe_fresh_repository):
    recipe_fresh_repository.add_recipe(create_recipe(name="test1"))
    recipe_fresh_repository.add_recipe(create_recipe(name="test2"))
    recipe_fresh_repository.add_recipe(create_recipe(name="test3"))
    res = client.get("/recipes")

    assert res.status_code == 200
    assert len(res.json()) == 3
    assert {r["name"] for r in res.json()} == {"test1", "test2", "test3"}


def test_get_recipe_successful(recipe_fresh_repository):
    recipe_fresh_repository.add_recipe(create_recipe(name="test1"))
    res = client.get("/recipes/1")

    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "name": "test1",
        "required_ingredients": ["eggs", "butter"],
    }
    assert len(res.json()) == 3


def test_get_recipe_not_found(recipe_fresh_repository):
    res = client.get("/recipes/99")

    assert res.status_code == 404
    assert res.json() == {"detail": "Recipe 99 not found"}


def test_update_recipe(recipe_fresh_repository):
    recipe_fresh_repository.add_recipe(create_recipe(name="test1"))
    payload = {
        "name": "updated_name",
        "required_ingredients": ["updated_ingredient"],
    }
    res = client.put("/recipes/1", json=payload)

    assert res.status_code == 200
    assert res.json()["name"] == "updated_name"
    assert res.json()["required_ingredients"] == ["updated_ingredient"]


def test_update_recipe_not_found(recipe_fresh_repository):
    res = client.put("/recipes/99", json={})
    assert res.status_code == 404
    assert res.json() == {"detail": "Recipe 99 not found"}


def test_delete_recipe(recipe_fresh_repository):
    recipe = recipe_fresh_repository.add_recipe(create_recipe(name="test1"))
    res = client.delete(f"/recipes/{recipe.id}")

    assert res.status_code == 204


def test_delete_recipe_not_found(recipe_fresh_repository):
    res = client.delete("/recipes/99")
    assert res.status_code == 404
    assert res.json() == {"detail": "Recipe 99 not found"}


def test_get_recipe_matches(fresh_repository, recipe_fresh_repository):
    fresh_repository.add_item(utils.create_item(name="Milk"))
    fresh_repository.add_item(utils.create_item(name="Eggs"))

    recipe_fresh_repository.add_recipe(
        Recipe(
            name="Scrambled Eggs",
            required_ingredients=["Eggs"],
        )
    )

    recipe_fresh_repository.add_recipe(
        Recipe(
            name="Omelette",
            required_ingredients=["Eggs", "Milk", "Cheese"],
        )
    )

    recipe_fresh_repository.add_recipe(
        Recipe(
            name="Pancakes",
            required_ingredients=["Milk", "Flour", "Sugar"],
        )
    )

    res = client.get("/recipes/matches")

    assert res.status_code == 200
    data = res.json()

    assert [recipe["name"] for recipe in data] == [
        "Scrambled Eggs",
        "Omelette",
        "Pancakes",
    ]
    assert data[1]["missing_ingredients"] == ["Cheese"]
    assert data[2]["missing_ingredients"] == ["Flour", "Sugar"]
