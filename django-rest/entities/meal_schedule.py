"""
MealSchedule Entity
Similar to @Entity class in Spring Boot JPA
"""

from django.db import models
from .recipe import Recipe


class MealSchedule(models.Model):
    """
    Represents a scheduled meal for a specific day and meal type

    Equivalent Spring Boot JPA:
    @Entity
    @Table(name = "meal_schedules")
    public class MealSchedule {
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private String mealName;
        private String dayOfWeek;
        private MealType mealType;

        @ManyToOne
        @JoinColumn(name = "recipe_id")
        private Recipe recipe;
    }
    """

    # Choices for day of week (like Enum in Java)
    class DayOfWeek(models.TextChoices):
        MONDAY = 'MONDAY', 'Monday'
        TUESDAY = 'TUESDAY', 'Tuesday'
        WEDNESDAY = 'WEDNESDAY', 'Wednesday'
        THURSDAY = 'THURSDAY', 'Thursday'
        FRIDAY = 'FRIDAY', 'Friday'
        SATURDAY = 'SATURDAY', 'Saturday'
        SUNDAY = 'SUNDAY', 'Sunday'

    # Choices for meal type (like Enum in Java)
    class MealType(models.TextChoices):
        BREAKFAST = 'BREAKFAST', 'Breakfast'
        LUNCH = 'LUNCH', 'Lunch'
        DINNER = 'DINNER', 'Dinner'

    meal_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Name of the meal being scheduled"
    )

    day_of_week = models.CharField(
        max_length=10,
        choices=DayOfWeek.choices,
        null=False,
        blank=False,
        help_text="Day of the week for this meal"
    )

    meal_type = models.CharField(
        max_length=10,
        choices=MealType.choices,
        null=False,
        blank=False,
        help_text="Type of meal (breakfast, lunch, or dinner)"
    )

    # Optional reference to a recipe
    # If user selects from existing recipes, this will be populated
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_meals',
        help_text="Optional reference to a recipe"
    )

    scheduled_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional: specific date for the meal"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes for this scheduled meal"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meal_schedules'
        ordering = ['day_of_week', 'meal_type']
        # Optionally prevent duplicate meals for same day/type
        # unique_together = ['day_of_week', 'meal_type']

    def __str__(self):
        return f"{self.day_of_week} {self.meal_type}: {self.meal_name}"

    def __repr__(self):
        return f"MealSchedule(id={self.id}, day='{self.day_of_week}', type='{self.meal_type}', meal='{self.meal_name}')"
