"""
MealSchedule Service
Similar to @Service class in Spring Boot
"""

from typing import List, Optional
from repositories import MealScheduleRepository, RecipeRepository
from entities.meal_schedule import MealSchedule


class MealScheduleService:
    """
    Service layer for MealSchedule business logic
    """

    def __init__(self):
        self.meal_schedule_repository = MealScheduleRepository()
        self.recipe_repository = RecipeRepository()

    def get_all_schedules(self) -> List[MealSchedule]:
        """
        Get all meal schedules
        """
        return self.meal_schedule_repository.find_all()

    def get_schedule_by_id(self, schedule_id: int) -> Optional[MealSchedule]:
        """
        Get meal schedule by ID
        """
        return self.meal_schedule_repository.find_by_id(schedule_id)

    def get_weekly_schedule(self) -> List[MealSchedule]:
        """
        Get the entire week's meal schedule
        """
        return self.meal_schedule_repository.get_weekly_schedule()

    def get_schedules_by_day(self, day: str) -> List[MealSchedule]:
        """
        Get all meals for a specific day
        """
        # Validate day
        valid_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        if day.upper() not in valid_days:
            raise ValueError(f"Invalid day. Must be one of: {', '.join(valid_days)}")

        return self.meal_schedule_repository.find_by_day_of_week(day)

    def get_schedules_by_meal_type(self, meal_type: str) -> List[MealSchedule]:
        """
        Get all meals of a specific type
        """
        # Validate meal type
        valid_types = ['BREAKFAST', 'LUNCH', 'DINNER']
        if meal_type.upper() not in valid_types:
            raise ValueError(f"Invalid meal type. Must be one of: {', '.join(valid_types)}")

        return self.meal_schedule_repository.find_by_meal_type(meal_type)

    def schedule_meal(self, meal_name: str, day_of_week: str, meal_type: str,
                     recipe_id: int = None, notes: str = None) -> MealSchedule:
        """
        Schedule a new meal
        Business logic: validate inputs, check recipe exists if provided
        """
        # Validation
        if not meal_name or meal_name.strip() == "":
            raise ValueError("Meal name cannot be empty")

        valid_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        if day_of_week.upper() not in valid_days:
            raise ValueError(f"Invalid day. Must be one of: {', '.join(valid_days)}")

        valid_types = ['BREAKFAST', 'LUNCH', 'DINNER']
        if meal_type.upper() not in valid_types:
            raise ValueError(f"Invalid meal type. Must be one of: {', '.join(valid_types)}")

        # Check if recipe exists if provided
        recipe = None
        if recipe_id:
            recipe = self.recipe_repository.find_by_id(recipe_id)
            if not recipe:
                raise ValueError(f"Recipe with id {recipe_id} not found")

        # Check if a meal is already scheduled for this day and type
        existing = self.meal_schedule_repository.find_by_day_and_type(day_of_week, meal_type)
        if existing:
            raise ValueError(f"A meal is already scheduled for {day_of_week} {meal_type}. Please update or delete it first.")

        meal_schedule = MealSchedule(
            meal_name=meal_name.strip(),
            day_of_week=day_of_week.upper(),
            meal_type=meal_type.upper(),
            recipe=recipe,
            notes=notes
        )
        return self.meal_schedule_repository.save(meal_schedule)

    def update_schedule(self, schedule_id: int, meal_name: str = None,
                       day_of_week: str = None, meal_type: str = None,
                       recipe_id: int = None, notes: str = None) -> Optional[MealSchedule]:
        """
        Update an existing meal schedule
        """
        schedule = self.meal_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            return None

        if meal_name is not None:
            if meal_name.strip() == "":
                raise ValueError("Meal name cannot be empty")
            schedule.meal_name = meal_name.strip()

        if day_of_week is not None:
            valid_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
            if day_of_week.upper() not in valid_days:
                raise ValueError(f"Invalid day. Must be one of: {', '.join(valid_days)}")
            schedule.day_of_week = day_of_week.upper()

        if meal_type is not None:
            valid_types = ['BREAKFAST', 'LUNCH', 'DINNER']
            if meal_type.upper() not in valid_types:
                raise ValueError(f"Invalid meal type. Must be one of: {', '.join(valid_types)}")
            schedule.meal_type = meal_type.upper()

        if recipe_id is not None:
            recipe = self.recipe_repository.find_by_id(recipe_id)
            if not recipe:
                raise ValueError(f"Recipe with id {recipe_id} not found")
            schedule.recipe = recipe

        if notes is not None:
            schedule.notes = notes

        return self.meal_schedule_repository.save(schedule)

    def delete_schedule(self, schedule_id: int) -> bool:
        """
        Delete a meal schedule
        """
        return self.meal_schedule_repository.delete_by_id(schedule_id)

    def clear_day_schedule(self, day: str):
        """
        Clear all meals scheduled for a specific day
        """
        schedules = self.get_schedules_by_day(day)
        for schedule in schedules:
            self.meal_schedule_repository.delete_by_id(schedule.id)
