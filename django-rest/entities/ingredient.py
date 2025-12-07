"""
Ingredient Entity
Similar to @Entity class in Spring Boot JPA

In Python/Django:
- Models inherit from models.Model (like @Entity in Spring)
- Fields are defined as class attributes (like @Column in JPA)
- No need for @Id annotation - Django creates 'id' automatically
- Foreign keys use models.ForeignKey (like @ManyToOne in JPA)
"""

from django.db import models


class Ingredient(models.Model):
    """
    Represents an ingredient in the inventory/stock

    Equivalent Spring Boot JPA entity:
    @Entity
    @Table(name = "ingredients")
    public class Ingredient {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @Column(nullable = false)
        private String name;

        private Double unitsAvailable;
        private String unitType;
    }
    """

    # Primary key is auto-created by Django as 'id' field
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Name of the ingredient (e.g., Tomato, Rice)"
    )

    units_available = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Quantity available in stock"
    )

    unit_type = models.CharField(
        max_length=50,
        default="pieces",
        help_text="Unit of measurement (e.g., kg, pieces, liters)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Database table name (like @Table(name="ingredients"))
        db_table = 'ingredients'
        # Default ordering
        ordering = ['name']

    def __str__(self):
        """
        String representation (like toString() in Java)
        """
        return f"{self.name} ({self.units_available} {self.unit_type})"

    def __repr__(self):
        return f"Ingredient(id={self.id}, name='{self.name}', units={self.units_available})"
