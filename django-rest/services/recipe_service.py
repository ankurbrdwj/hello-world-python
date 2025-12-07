"""
Recipe Service
Similar to @Service class in Spring Boot
"""

from typing import List, Optional, Dict
from repositories import RecipeRepository, RecipeIngredientRepository, IngredientRepository
from entities.recipe import Recipe, RecipeIngredient


class RecipeService:
    """
    Service layer for Recipe business logic
    """

    def __init__(self):
        self.recipe_repository = RecipeRepository()
        self.recipe_ingredient_repository = RecipeIngredientRepository()
        self.ingredient_repository = IngredientRepository()

    def get_all_recipes(self) -> List[Recipe]:
        """
        Get all recipes
        """
        return self.recipe_repository.find_all()

    def get_recipe_by_id(self, recipe_id: int) -> Optional[Recipe]:
        """
        Get recipe by ID with all ingredients
        """
        return self.recipe_repository.find_by_id(recipe_id)

    def create_recipe(self, meal_name: str, description: str = None,
                     web_link: str = None) -> Recipe:
        """
        Create a new recipe
        Business validation
        """
        if not meal_name or meal_name.strip() == "":
            raise ValueError("Meal name cannot be empty")

        recipe = Recipe(
            meal_name=meal_name.strip(),
            description=description,
            web_link=web_link
        )
        return self.recipe_repository.save(recipe)

    def update_recipe(self, recipe_id: int, meal_name: str = None,
                     description: str = None, web_link: str = None) -> Optional[Recipe]:
        """
        Update an existing recipe
        """
        recipe = self.recipe_repository.find_by_id(recipe_id)
        if not recipe:
            return None

        if meal_name is not None:
            if meal_name.strip() == "":
                raise ValueError("Meal name cannot be empty")
            recipe.meal_name = meal_name.strip()

        if description is not None:
            recipe.description = description

        if web_link is not None:
            recipe.web_link = web_link

        return self.recipe_repository.save(recipe)

    def delete_recipe(self, recipe_id: int) -> bool:
        """
        Delete a recipe
        """
        return self.recipe_repository.delete_by_id(recipe_id)

    def add_ingredient_to_recipe(self, recipe_id: int, ingredient_id: int,
                                quantity: str) -> RecipeIngredient:
        """
        Add an ingredient to a recipe with quantity
        Business logic: validate recipe and ingredient exist
        """
        recipe = self.recipe_repository.find_by_id(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe with id {recipe_id} not found")

        ingredient = self.ingredient_repository.find_by_id(ingredient_id)
        if not ingredient:
            raise ValueError(f"Ingredient with id {ingredient_id} not found")

        if not quantity or quantity.strip() == "":
            raise ValueError("Quantity cannot be empty")

        recipe_ingredient = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            quantity=quantity.strip()
        )
        return self.recipe_ingredient_repository.save(recipe_ingredient)

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        """
        Get all ingredients for a specific recipe
        """
        return self.recipe_ingredient_repository.find_by_recipe_id(recipe_id)

    def remove_all_ingredients_from_recipe(self, recipe_id: int):
        """
        Remove all ingredients from a recipe
        Useful when updating recipe ingredients
        """
        self.recipe_ingredient_repository.delete_by_recipe_id(recipe_id)

    def search_recipes_by_name(self, meal_name: str) -> List[Recipe]:
        """
        Search recipes by meal name
        """
        if not meal_name or meal_name.strip() == "":
            return self.get_all_recipes()
        return self.recipe_repository.find_by_meal_name_containing(meal_name.strip())

    def get_recipe_with_ingredients_detail(self, recipe_id: int) -> Optional[Dict]:
        """
        Get recipe with full ingredient details
        Business logic: format data for API response
        """
        recipe = self.recipe_repository.find_by_id(recipe_id)
        if not recipe:
            return None

        recipe_ingredients = self.recipe_ingredient_repository.find_by_recipe_id(recipe_id)

        return {
            'id': recipe.id,
            'meal_name': recipe.meal_name,
            'description': recipe.description,
            'web_link': recipe.web_link,
            'ingredients': [
                {
                    'ingredient_id': ri.ingredient.id,
                    'ingredient_name': ri.ingredient.name,
                    'quantity': ri.quantity,
                    'unit_type': ri.ingredient.unit_type
                }
                for ri in recipe_ingredients
            ]
        }
