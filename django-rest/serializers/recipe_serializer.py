"""
Recipe Serializer
Similar to DTOs in Spring Boot for complex nested objects
"""

from rest_framework import serializers
from entities.recipe import Recipe, RecipeIngredient
from entities.ingredient import Ingredient


class RecipeIngredientSerializer(serializers.Serializer):
    """
    Serializer for RecipeIngredient join table
    """
    ingredient_id = serializers.IntegerField()
    ingredient_name = serializers.CharField(read_only=True, source='ingredient.name')
    quantity = serializers.CharField(max_length=100)
    unit_type = serializers.CharField(read_only=True, source='ingredient.unit_type')


class RecipeSerializer(serializers.Serializer):
    """
    Serializer for Recipe entity
    """
    id = serializers.IntegerField(read_only=True)
    meal_name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    web_link = serializers.URLField(max_length=500, required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_meal_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip()


class RecipeDetailSerializer(serializers.Serializer):
    """
    Detailed recipe serializer with ingredients
    Similar to a DTO with nested objects in Spring Boot
    """
    id = serializers.IntegerField(read_only=True)
    meal_name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    web_link = serializers.URLField(max_length=500, required=False, allow_blank=True, allow_null=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True, source='recipeingredient_set')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class RecipeCreateSerializer(serializers.Serializer):
    """
    Request DTO for creating recipe
    """
    meal_name = serializers.CharField(max_length=200, required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    web_link = serializers.URLField(max_length=500, required=False, allow_blank=True, allow_null=True)

    def validate_meal_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip()


class RecipeUpdateSerializer(serializers.Serializer):
    """
    Request DTO for updating recipe
    All fields optional
    """
    meal_name = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    web_link = serializers.URLField(max_length=500, required=False, allow_blank=True, allow_null=True)

    def validate_meal_name(self, value):
        if value and value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip() if value else value


class AddIngredientToRecipeSerializer(serializers.Serializer):
    """
    Request DTO for adding ingredient to recipe
    """
    ingredient_id = serializers.IntegerField(required=True)
    quantity = serializers.CharField(max_length=100, required=True)

    def validate_quantity(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Quantity cannot be empty")
        return value.strip()
