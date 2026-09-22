from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user, get_recipe_repository
from app.domain.recipe import Recipe
from app.domain.user import User
from app.schemas import RecipeCreate, RecipeRead, RecipeUpdate

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


@router.get("/recipes", response_model=list[RecipeRead], status_code=status.HTTP_200_OK)
def list_recipes(
    repository=Depends(get_recipe_repository),
    current_user: User = Depends(get_current_user),
) -> list[RecipeRead]:
    recipes = repository.list_all()
    recipes_for_return = [_recipe_to_read(recipe) for recipe in recipes]
    return sorted(recipes_for_return, key=lambda recipe: recipe.name)


@router.get(
    "/recipes/{recipe_id}", response_model=RecipeRead, status_code=status.HTTP_200_OK
)
def read_recipe(
    recipe_id: int,
    repository=Depends(get_recipe_repository),
    current_user: User = Depends(get_current_user),
) -> RecipeRead:
    recipe = repository.get_recipe(recipe_id)
    return _recipe_to_read(recipe)


@router.put(
    "/recipes/{recipe_id}", response_model=RecipeRead, status_code=status.HTTP_200_OK
)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    repository=Depends(get_recipe_repository),
    current_user: User = Depends(get_current_user),
) -> RecipeRead:
    payload = recipe_update.model_dump(exclude_unset=True)
    updated_recipe = repository.update_recipe(recipe_id, payload)
    return _recipe_to_read(updated_recipe)


@router.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    repository=Depends(get_recipe_repository),
    current_user: User = Depends(get_current_user),
) -> None:
    repository.delete_recipe(recipe_id)
