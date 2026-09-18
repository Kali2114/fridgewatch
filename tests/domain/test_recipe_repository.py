import pytest

from app.domain.exceptions import RecipeNotFound
from app.domain.recipe_repository import InMemoryRecipeRepository
from tests.domain.utils import create_recipe


class TestInMemoryRecipeRepository:
    def setup_method(self):
        self.repository = InMemoryRecipeRepository()
        self.recipe = create_recipe()
        self.added = self.repository.add_recipe(self.recipe)

    def test_add_recipe(self):
        assert self.recipe is self.added
        assert self.recipe.id == 1

    def test_get_recipe(self):
        retrieved = self.repository.get_recipe(1)
        assert retrieved is self.recipe

    def test_get_recipe_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.get_recipe(99)

    def test_second_add_get_next_id(self):
        recipe = self.repository.add_recipe(create_recipe(name="second recipe"))
        assert recipe.id == 2

    def test_delete_recipe(self):
        self.repository.delete_recipe(1)

        with pytest.raises(RecipeNotFound):
            self.repository.get_recipe(1)

    def test_delete_recipe_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.delete_recipe(99)

    def test_list_all_recipes(self):
        self.repository.add_recipe(create_recipe(name="second recipe"))
        self.repository.add_recipe(create_recipe(name="third recipe"))
        result = self.repository.list_all_recipes()

        assert len(result) == 3

    def test_update_recipe(self):
        payload = {
            "name": "updated_name",
            "required_ingredients": ["updated1", "updated2"],
        }
        self.repository.update_recipe(1, payload)

        assert self.repository.get_recipe(1).name == payload["name"]
        assert (
            self.repository.get_recipe(1).required_ingredients
            == payload["required_ingredients"]
        )

    def test_update_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.update_recipe(99, {"name": "updated_name"})

    def test_update_recipe_invalid_ingredients(self):
        payload = {"name": "updated_name", "required_ingredients": []}
        with pytest.raises(ValueError):
            self.repository.update_recipe(1, payload)
