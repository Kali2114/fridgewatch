from typing import Any

from app.domain.exceptions import RecipeNotFound
from app.domain.recipe import Recipe


class InMemoryRecipeRepository:
    def __init__(self) -> None:
        self.recipes: dict[int, Recipe] = {}
        self._id = 1

    def add_recipe(self, recipe: Recipe) -> Recipe:
        recipe.id = self._id
        self.recipes[recipe.id] = recipe
        self._id += 1
        return recipe

    def get_recipe(self, recipe_id: int) -> Recipe:
        try:
            return self.recipes[recipe_id]
        except KeyError:
            raise RecipeNotFound(f"Recipe with id {recipe_id} not found") from None

    def delete_recipe(self, recipe_id: int) -> None:
        try:
            del self.recipes[recipe_id]
        except KeyError:
            raise RecipeNotFound(f"Recipe with id {recipe_id} not found") from None

    def list_all_recipes(self) -> list[Recipe]:
        return list(self.recipes.values())

    def update_recipe(self, recipe_id: int, payload: dict[str, Any]) -> Recipe:
        recipe = self.get_recipe(recipe_id)
        for key, value in payload.items():
            setattr(recipe, key, value)
        return recipe
