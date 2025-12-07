"""
Ingredient Service
Similar to @Service class in Spring Boot

In Spring Boot:
@Service
public class IngredientService {
    @Autowired
    private IngredientRepository ingredientRepository;

    public List<Ingredient> getAllIngredients() {
        return ingredientRepository.findAll();
    }
}
"""

from typing import List, Optional
from repositories import IngredientRepository
from entities.ingredient import Ingredient


class IngredientService:
    """
    Service layer for Ingredient business logic
    Similar to @Service in Spring Boot
    """

    def __init__(self):
        self.repository = IngredientRepository()

    def get_all_ingredients(self) -> List[Ingredient]:
        """
        Get all ingredients
        Business logic can be added here (e.g., sorting, filtering)
        """
        return self.repository.find_all()

    def get_ingredient_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        """
        Get ingredient by ID
        """
        return self.repository.find_by_id(ingredient_id)

    def get_ingredients_in_stock(self) -> List[Ingredient]:
        """
        Get only ingredients that are available in stock
        Business logic: filter by units_available > 0
        """
        return self.repository.find_in_stock()

    def create_ingredient(self, name: str, units_available: float, unit_type: str) -> Ingredient:
        """
        Create a new ingredient
        Business logic: validation can be added here
        """
        # Business validation
        if not name or name.strip() == "":
            raise ValueError("Ingredient name cannot be empty")

        if units_available < 0:
            raise ValueError("Units available cannot be negative")

        ingredient = Ingredient(
            name=name.strip(),
            units_available=units_available,
            unit_type=unit_type
        )
        return self.repository.save(ingredient)

    def update_ingredient(self, ingredient_id: int, name: str = None,
                         units_available: float = None, unit_type: str = None) -> Optional[Ingredient]:
        """
        Update an existing ingredient
        Business logic: partial updates allowed
        """
        ingredient = self.repository.find_by_id(ingredient_id)
        if not ingredient:
            return None

        if name is not None:
            if name.strip() == "":
                raise ValueError("Ingredient name cannot be empty")
            ingredient.name = name.strip()

        if units_available is not None:
            if units_available < 0:
                raise ValueError("Units available cannot be negative")
            ingredient.units_available = units_available

        if unit_type is not None:
            ingredient.unit_type = unit_type

        return self.repository.save(ingredient)

    def delete_ingredient(self, ingredient_id: int) -> bool:
        """
        Delete an ingredient
        Business logic: could check if ingredient is used in recipes
        """
        return self.repository.delete_by_id(ingredient_id)

    def search_ingredients_by_name(self, name: str) -> List[Ingredient]:
        """
        Search ingredients by name
        """
        if not name or name.strip() == "":
            return self.get_all_ingredients()
        return self.repository.find_by_name_containing(name.strip())

    def update_stock(self, ingredient_id: int, quantity_change: float) -> Optional[Ingredient]:
        """
        Update ingredient stock (add or subtract)
        Business logic: prevent negative stock
        """
        ingredient = self.repository.find_by_id(ingredient_id)
        if not ingredient:
            return None

        new_quantity = float(ingredient.units_available) + quantity_change

        if new_quantity < 0:
            raise ValueError(f"Insufficient stock. Available: {ingredient.units_available}, Requested: {abs(quantity_change)}")

        ingredient.units_available = new_quantity
        return self.repository.save(ingredient)
