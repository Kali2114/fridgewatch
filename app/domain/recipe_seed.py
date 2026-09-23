from app.domain.recipe import Recipe

SEED_RECIPES = [
    {"name": "Scrambled Eggs", "required_ingredients": ["eggs", "butter"]},
    {"name": "Omelette", "required_ingredients": ["eggs", "milk", "cheese"]},
    {
        "name": "Pancakes",
        "required_ingredients": ["flour", "milk", "eggs", "sugar", "butter"],
    },
    {
        "name": "Grilled Cheese Sandwich",
        "required_ingredients": ["bread", "cheese", "butter"],
    },
    {
        "name": "Spaghetti Aglio e Olio",
        "required_ingredients": ["pasta", "garlic", "olive oil"],
    },
    {"name": "Tomato Soup", "required_ingredients": ["tomatoes", "onion", "garlic"]},
    {
        "name": "Caesar Salad",
        "required_ingredients": ["lettuce", "chicken", "parmesan"],
    },
    {"name": "Fried Rice", "required_ingredients": ["rice", "eggs", "soy sauce"]},
]


def seed_recipes(repository) -> None:
    if repository.list_all():
        return
    for data in SEED_RECIPES:
        repository.add_recipe(Recipe(**data))
