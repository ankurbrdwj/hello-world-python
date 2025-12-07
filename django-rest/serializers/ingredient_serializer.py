"""
Ingredient Serializer
Similar to DTO in Spring Boot

In Spring Boot you would create DTOs:
public class IngredientDTO {
    private Long id;
    private String name;
    private Double unitsAvailable;
    private String unitType;
    // getters and setters
}

In Django REST Framework, serializers handle:
- Converting model instances to JSON (serialization)
- Converting JSON to model instances (deserialization)
- Validation
"""

from rest_framework import serializers
from entities.ingredient import Ingredient


class IngredientSerializer(serializers.Serializer):
    """
    Serializer for Ingredient entity
    Manual field definition (like creating a DTO class)
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    units_available = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    unit_type = serializers.CharField(max_length=50, default="pieces")
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new Ingredient instance
        """
        return Ingredient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Ingredient instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.units_available = validated_data.get('units_available', instance.units_available)
        instance.unit_type = validated_data.get('unit_type', instance.unit_type)
        instance.save()
        return instance

    def validate_name(self, value):
        """
        Custom validation for name field
        Similar to @NotBlank validation in Spring Boot
        """
        if not value or value.strip() == "":
            raise serializers.ValidationError("Ingredient name cannot be empty")
        return value.strip()

    def validate_units_available(self, value):
        """
        Custom validation for units_available
        Similar to @Min(0) validation in Spring Boot
        """
        if value < 0:
            raise serializers.ValidationError("Units available cannot be negative")
        return value


class IngredientCreateSerializer(serializers.Serializer):
    """
    Request DTO for creating ingredient
    Only includes fields needed for creation
    """
    name = serializers.CharField(max_length=100, required=True)
    units_available = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    unit_type = serializers.CharField(max_length=50, default="pieces")

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Ingredient name cannot be empty")
        return value.strip()

    def validate_units_available(self, value):
        if value < 0:
            raise serializers.ValidationError("Units available cannot be negative")
        return value


class IngredientUpdateSerializer(serializers.Serializer):
    """
    Request DTO for updating ingredient
    All fields are optional
    """
    name = serializers.CharField(max_length=100, required=False)
    units_available = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False
    )
    unit_type = serializers.CharField(max_length=50, required=False)

    def validate_name(self, value):
        if value and value.strip() == "":
            raise serializers.ValidationError("Ingredient name cannot be empty")
        return value.strip() if value else value

    def validate_units_available(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Units available cannot be negative")
        return value
