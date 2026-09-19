from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user, get_recipe_repository
from app.domain.recipe import Recipe
from app.domain.user import User
from app.schemas import RecipeCreate, RecipeRead

router = APIRouter()


def _recipe_to_read(recipe: Recipe) -> RecipeRead:
    return RecipeRead(
        id=recipe.id,
        name=recipe.name,
        required_ingredients=recipe.required_ingredients,
    )


@router.post("/recipes", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
def create_recipe(
    recipe: RecipeCreate,
    repository=Depends(get_recipe_repository),
    current_user: User = Depends(get_current_user),
) -> RecipeRead:
    recipe_created = Recipe(
        name=recipe.name,
        required_ingredients=recipe.required_ingredients,
    )
    repository.add_recipe(recipe_created)
    new_recipe = _recipe_to_read(recipe_created)
    return new_recipe
