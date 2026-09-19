import pytest

from app.domain.exceptions import RecipeNotFound
from app.infrastructure.recipe_repository import SQLAlchemyRecipeRepository
from tests.domain.utils import create_recipe


class TestSQLAlchemyRecipeRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = SQLAlchemyRecipeRepository(db_session)

    def test_add_recipe(self):
        recipe = create_recipe()
        added_recipe = self.repository.add_recipe(recipe)

        assert recipe is added_recipe
        assert recipe.id is not None

    def test_get_recipe(self):
        recipe = create_recipe()
        self.repository.add_recipe(recipe)
        retrieved = self.repository.get_recipe(recipe.id)

        assert recipe.id == retrieved.id
        assert recipe.name == retrieved.name
        assert recipe.required_ingredients == retrieved.required_ingredients

    def test_get_recipe_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.get_recipe(99)

    def test_delete_recipe(self):
        recipe = create_recipe()
        self.repository.add_recipe(recipe)
        self.repository.delete_recipe(recipe.id)

        with pytest.raises(RecipeNotFound):
            self.repository.get_recipe(recipe.id)

    def test_delete_recipe_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.delete_recipe(99)

    def test_update_recipe(self):
        recipe = create_recipe()
        self.repository.add_recipe(recipe)
        payload = {
            "name": "Updated recipe",
            "required_ingredients": ["updated ingredient"],
        }
        updated_recipe = self.repository.update_recipe(recipe.id, payload)

        assert updated_recipe.id == recipe.id
        assert updated_recipe.name == payload["name"]
        assert updated_recipe.required_ingredients == payload["required_ingredients"]

    def test_update_recipe_not_found(self):
        with pytest.raises(RecipeNotFound):
            self.repository.update_recipe(99, {})

    def test_list_all(self):
        self.repository.add_recipe(create_recipe(name="first recipe"))
        self.repository.add_recipe(create_recipe(name="second recipe"))
        result = self.repository.list_all()

        assert len(result) == 2
        assert [recipe.name for recipe in result] == ["first recipe", "second recipe"]
