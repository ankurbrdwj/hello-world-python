"""
Ingredient Repository
Similar to JpaRepository<Ingredient, Long> in Spring Boot

In Spring Boot you would write:
public interface IngredientRepository extends JpaRepository<Ingredient, Long> {
    List<Ingredient> findByNameContaining(String name);
}

In Django, repositories are implemented as classes that wrap QuerySet operations
"""

from typing import List, Optional
from entities.ingredient import Ingredient


class IngredientRepository:
    """
    Repository pattern for Ingredient entity
    Provides data access layer abstraction
    """

    @staticmethod
    def find_all() -> List[Ingredient]:
        """
        Get all ingredients
        Equivalent to: ingredientRepository.findAll() in Spring Boot
        """
        return list(Ingredient.objects.all())

    @staticmethod
    def find_by_id(ingredient_id: int) -> Optional[Ingredient]:
        """
        Find ingredient by ID
        Equivalent to: ingredientRepository.findById(id) in Spring Boot
        """
        try:
            return Ingredient.objects.get(id=ingredient_id)
        except Ingredient.DoesNotExist:
            return None

    @staticmethod
    def save(ingredient: Ingredient) -> Ingredient:
        """
        Save or update ingredient
        Equivalent to: ingredientRepository.save(ingredient) in Spring Boot
        """
        ingredient.save()
        return ingredient

    @staticmethod
    def delete_by_id(ingredient_id: int) -> bool:
        """
        Delete ingredient by ID
        Equivalent to: ingredientRepository.deleteById(id) in Spring Boot
        Returns True if deleted, False if not found
        """
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.delete()
            return True
        except Ingredient.DoesNotExist:
            return False

    @staticmethod
    def find_by_name_containing(name: str) -> List[Ingredient]:
        """
        Find ingredients by name (case-insensitive partial match)
        Equivalent to: ingredientRepository.findByNameContaining(name) in Spring Boot
        """
        return list(Ingredient.objects.filter(name__icontains=name))

    @staticmethod
    def find_in_stock() -> List[Ingredient]:
        """
        Find ingredients that are in stock (units_available > 0)
        Custom query method
        """
        return list(Ingredient.objects.filter(units_available__gt=0))

    @staticmethod
    def exists_by_id(ingredient_id: int) -> bool:
        """
        Check if ingredient exists by ID
        Equivalent to: ingredientRepository.existsById(id) in Spring Boot
        """
        return Ingredient.objects.filter(id=ingredient_id).exists()

    @staticmethod
    def count() -> int:
        """
        Count total ingredients
        Equivalent to: ingredientRepository.count() in Spring Boot
        """
        return Ingredient.objects.count()
