"""
URL Configuration
Similar to @RequestMapping in Spring Boot

In Spring Boot:
@RestController
@RequestMapping("/api/ingredients")
public class IngredientController { ... }

In Django, we define URL patterns here
"""

from django.contrib import admin
from django.urls import path
from controllers import (
    IngredientController,
    IngredientSearchController,
    RecipeController,
    RecipeIngredientController,
    RecipeSearchController,
    MealScheduleController
)

urlpatterns = [
    # Admin interface (like Spring Boot Actuator)
    path('admin/', admin.site.urls),

    # Ingredient endpoints
    path('api/ingredients/', IngredientController.as_view(), name='ingredient-list-create'),
    path('api/ingredients/<int:ingredient_id>/', IngredientController.as_view(), name='ingredient-detail'),
    path('api/ingredients/search/', IngredientSearchController.as_view(), name='ingredient-search'),

    # Recipe endpoints
    path('api/recipes/', RecipeController.as_view(), name='recipe-list-create'),
    path('api/recipes/<int:recipe_id>/', RecipeController.as_view(), name='recipe-detail'),
    path('api/recipes/search/', RecipeSearchController.as_view(), name='recipe-search'),
    path('api/recipes/<int:recipe_id>/ingredients/', RecipeIngredientController.as_view(), name='recipe-add-ingredient'),

    # Meal Schedule endpoints
    path('api/meal-schedule/', MealScheduleController.as_view(), name='meal-schedule-list-create'),
    path('api/meal-schedule/<int:schedule_id>/', MealScheduleController.as_view(), name='meal-schedule-detail'),
]
