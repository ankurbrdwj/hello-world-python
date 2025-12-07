"""
MealSchedule Serializer
Similar to DTOs in Spring Boot
"""

from rest_framework import serializers
from entities.meal_schedule import MealSchedule


class MealScheduleSerializer(serializers.Serializer):
    """
    Serializer for MealSchedule entity
    """
    id = serializers.IntegerField(read_only=True)
    meal_name = serializers.CharField(max_length=200, required=True)
    day_of_week = serializers.ChoiceField(
        choices=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'],
        required=True
    )
    meal_type = serializers.ChoiceField(
        choices=['BREAKFAST', 'LUNCH', 'DINNER'],
        required=True
    )
    recipe_id = serializers.IntegerField(required=False, allow_null=True, source='recipe.id')
    recipe_name = serializers.CharField(read_only=True, source='recipe.meal_name')
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_meal_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip()


class MealScheduleCreateSerializer(serializers.Serializer):
    """
    Request DTO for creating meal schedule
    """
    meal_name = serializers.CharField(max_length=200, required=True)
    day_of_week = serializers.ChoiceField(
        choices=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'],
        required=True
    )
    meal_type = serializers.ChoiceField(
        choices=['BREAKFAST', 'LUNCH', 'DINNER'],
        required=True
    )
    recipe_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_meal_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip()


class MealScheduleUpdateSerializer(serializers.Serializer):
    """
    Request DTO for updating meal schedule
    All fields optional
    """
    meal_name = serializers.CharField(max_length=200, required=False)
    day_of_week = serializers.ChoiceField(
        choices=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'],
        required=False
    )
    meal_type = serializers.ChoiceField(
        choices=['BREAKFAST', 'LUNCH', 'DINNER'],
        required=False
    )
    recipe_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_meal_name(self, value):
        if value and value.strip() == "":
            raise serializers.ValidationError("Meal name cannot be empty")
        return value.strip() if value else value
