"""
Recipe Entity
Similar to @Entity class in Spring Boot JPA with Many-to-Many relationship
"""

from django.db import models
from .ingredient import Ingredient


class Recipe(models.Model):
    """
    Represents a recipe with meal name, preparation instructions, and required ingredients

    Equivalent Spring Boot JPA:
    @Entity
    @Table(name = "recipes")
    public class Recipe {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private String mealName;
        private String description;
        private String webLink;

        @OneToMany(mappedBy = "recipe")
        private List<RecipeIngredient> recipeIngredients;
    }
    """

    meal_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Name of the meal (e.g., Chicken Curry, Pasta)"
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Full description of how to prepare the meal"
    )

    web_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional URL to external recipe website"
    )

    # Many-to-Many relationship with Ingredient
    # Through table allows us to store quantity for each ingredient
    # Similar to @ManyToMany with join table in Spring Boot
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        help_text="Ingredients required for this recipe"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recipes'
        ordering = ['meal_name']

    def __str__(self):
        return self.meal_name

    def __repr__(self):
        return f"Recipe(id={self.id}, meal_name='{self.meal_name}')"


class RecipeIngredient(models.Model):
    """
    Join table for Recipe and Ingredient with additional quantity field

    Equivalent Spring Boot JPA:
    @Entity
    @Table(name = "recipe_ingredients")
    public class RecipeIngredient {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @ManyToOne
        @JoinColumn(name = "recipe_id")
        private Recipe recipe;

        @ManyToOne
        @JoinColumn(name = "ingredient_id")
        private Ingredient ingredient;

        private String quantity;
    }
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        help_text="Reference to the recipe"
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        help_text="Reference to the ingredient"
    )

    quantity = models.CharField(
        max_length=100,
        help_text="Quantity needed (e.g., '2 pieces', '500g', '1 cup')"
    )

    class Meta:
        db_table = 'recipe_ingredients'
        # Ensure a recipe doesn't have duplicate ingredients
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return f"{self.recipe.meal_name} needs {self.quantity} of {self.ingredient.name}"

    def __repr__(self):
        return f"RecipeIngredient(recipe='{self.recipe.meal_name}', ingredient='{self.ingredient.name}', quantity='{self.quantity}')"
