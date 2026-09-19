from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import Session

from app.domain.exceptions import RecipeNotFound
from app.domain.recipe import Recipe
from app.infrastructure.models import RecipeModel


class SQLAlchemyRecipeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_recipe(self, recipe: Recipe) -> Recipe:
        model = RecipeModel(
            name=recipe.name,
            required_ingredients=recipe.required_ingredients,
        )
        self.session.add(model)
        self.session.commit()
        recipe.id = model.id
        return recipe

    def get_recipe(self, recipe_id: int) -> Recipe:
        model = self.session.get(RecipeModel, recipe_id)
        if model is None:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        return self._to_domain(model)

    def delete_recipe(self, recipe_id: int) -> None:
        model = self.session.get(RecipeModel, recipe_id)
        if model is None:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        self.session.delete(model)
        self.session.commit()

    def update_recipe(self, recipe_id: int, payload: dict[str, Any]) -> Recipe:
        model = self.session.get(RecipeModel, recipe_id)
        if model is None:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")

        domain_recipe = self._to_domain(model)
        for key, values in payload.items():
            setattr(domain_recipe, key, values)

        model.name = domain_recipe.name
        model.required_ingredients = domain_recipe.required_ingredients
        self.session.commit()
        return domain_recipe

    def list_all(self) -> list[Recipe]:
        statement = Select(RecipeModel)
        result = self.session.execute(statement)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: RecipeModel) -> Recipe:
        return Recipe(
            id=model.id,
            name=model.name,
            required_ingredients=model.required_ingredients,
        )
