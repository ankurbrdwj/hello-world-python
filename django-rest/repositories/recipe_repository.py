"""
Recipe Repository
Similar to JpaRepository<Recipe, Long> in Spring Boot
"""

from typing import List, Optional
from entities.recipe import Recipe, RecipeIngredient


class RecipeRepository:
    """
    Repository pattern for Recipe entity
    """

    @staticmethod
    def find_all() -> List[Recipe]:
        """
        Get all recipes with prefetched ingredients (optimization)
        Equivalent to: recipeRepository.findAll() in Spring Boot
        """
        return list(Recipe.objects.prefetch_related('ingredients').all())

    @staticmethod
    def find_by_id(recipe_id: int) -> Optional[Recipe]:
        """
        Find recipe by ID with ingredients
        Equivalent to: recipeRepository.findById(id) in Spring Boot
        """
        try:
            return Recipe.objects.prefetch_related('ingredients').get(id=recipe_id)
        except Recipe.DoesNotExist:
            return None

    @staticmethod
    def save(recipe: Recipe) -> Recipe:
        """
        Save or update recipe
        Equivalent to: recipeRepository.save(recipe) in Spring Boot
        """
        recipe.save()
        return recipe

    @staticmethod
    def delete_by_id(recipe_id: int) -> bool:
        """
        Delete recipe by ID
        Equivalent to: recipeRepository.deleteById(id) in Spring Boot
        """
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.delete()
            return True
        except Recipe.DoesNotExist:
            return False

    @staticmethod
    def find_by_meal_name_containing(meal_name: str) -> List[Recipe]:
        """
        Find recipes by meal name (case-insensitive)
        Equivalent to: recipeRepository.findByMealNameContaining(mealName) in Spring Boot
        """
        return list(Recipe.objects.filter(meal_name__icontains=meal_name))

    @staticmethod
    def exists_by_id(recipe_id: int) -> bool:
        """
        Check if recipe exists
        """
        return Recipe.objects.filter(id=recipe_id).exists()


class RecipeIngredientRepository:
    """
    Repository for RecipeIngredient join table
    """

    @staticmethod
    def save(recipe_ingredient: RecipeIngredient) -> RecipeIngredient:
        """
        Save recipe-ingredient relationship
        """
        recipe_ingredient.save()
        return recipe_ingredient

    @staticmethod
    def find_by_recipe_id(recipe_id: int) -> List[RecipeIngredient]:
        """
        Get all ingredients for a specific recipe
        """
        return list(RecipeIngredient.objects.filter(recipe_id=recipe_id).select_related('ingredient'))

    @staticmethod
    def delete_by_recipe_id(recipe_id: int):
        """
        Delete all ingredients for a recipe
        Useful when updating a recipe's ingredients
        """
        RecipeIngredient.objects.filter(recipe_id=recipe_id).delete()
