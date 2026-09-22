from app.domain.recipe_repository import InMemoryRecipeRepository
from app.domain.recipe_seed import SEED_RECIPES, seed_recipes


class TestSeedRecipes:
    def test_seeds_when_empty(self):
        repository = InMemoryRecipeRepository()

        seed_recipes(repository)

        assert len(repository.list_all()) == len(SEED_RECIPES)

    def test_does_not_reseed_when_not_empty(self):
        repository = InMemoryRecipeRepository()
        seed_recipes(repository)

        seed_recipes(repository)

        assert len(repository.list_all()) == len(SEED_RECIPES)
