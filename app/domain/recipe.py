from app.domain.inventory import Item


class Recipe:
    def __init__(
        self, name: str, required_ingredients: list[str], id: int | None = None
    ) -> None:
        self.name = name
        self.required_ingredients = required_ingredients
        self.id = id

    @property
    def required_ingredients(self) -> list[str]:
        return self._required_ingredients

    @required_ingredients.setter
    def required_ingredients(self, ingredients: list[str]) -> None:
        if not ingredients:
            raise ValueError("ingredients cannot be empty")
        self._required_ingredients = ingredients


def missing_ingredients(recipe: Recipe, items: list[Item]) -> set[str]:
    names = {item.name for item in items}
    result = set()
    for ingredient in recipe.required_ingredients:
        if ingredient not in names:
            result.add(ingredient)
    return result


def rank_recipes_by_missing_ingredients(
    recipes: list[Recipe], items: list[Item]
) -> list[Recipe]:
    return sorted(recipes, key=lambda recipe: len(missing_ingredients(recipe, items)))
