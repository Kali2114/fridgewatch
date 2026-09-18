from app.domain.recipe import (
    Recipe,
    missing_ingredients,
    rank_recipes_by_missing_ingredients,
)
from tests.domain.utils import create_item


class TestRecipe:
    def test_missing_ingredients_when_all_in_stock(self):
        item1 = create_item(name="milk")
        item2 = create_item(name="eggs")
        items = [item1, item2]
        recipe = Recipe(
            name="Omelette",
            required_ingredients=["eggs", "milk"],
        )
        result = missing_ingredients(recipe, items)

        assert result == set()

    def test_missing_ingredients_when_some_missing(self):
        item1 = create_item(name="eggs")
        item2 = create_item(name="butter")
        items = [item1, item2]
        recipe = Recipe(
            name="Scrambled Eggs",
            required_ingredients=["eggs", "butter", "onions", "tomatoes"],
        )
        result = missing_ingredients(recipe, items)

        assert result == {"onions", "tomatoes"}

    def test_recipes_are_ranked_by_fewest_missing_ingredients(self):
        item1 = create_item(name="eggs")
        item2 = create_item(name="butter")
        item3 = create_item(name="tomatoes")
        item4 = create_item(name="milk")
        items = [item1, item2, item3, item4]

        recipe1 = Recipe(
            name="Scrambled Eggs",
            required_ingredients=["eggs", "butter"],
        )

        recipe2 = Recipe(
            name="Omelette",
            required_ingredients=["eggs", "milk", "cheese"],
        )

        recipe3 = Recipe(
            name="Tomato Pasta",
            required_ingredients=["tomatoes", "pasta", "garlic", "cheese"],
        )
        recipes = [recipe1, recipe2, recipe3]
        result = rank_recipes_by_missing_ingredients(recipes, items)

        assert result == [recipe1, recipe2, recipe3]
