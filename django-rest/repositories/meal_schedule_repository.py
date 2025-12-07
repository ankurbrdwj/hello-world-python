"""
MealSchedule Repository
Similar to JpaRepository<MealSchedule, Long> in Spring Boot
"""

from typing import List, Optional
from entities.meal_schedule import MealSchedule


class MealScheduleRepository:
    """
    Repository pattern for MealSchedule entity
    """

    @staticmethod
    def find_all() -> List[MealSchedule]:
        """
        Get all scheduled meals
        Equivalent to: mealScheduleRepository.findAll() in Spring Boot
        """
        return list(MealSchedule.objects.select_related('recipe').all())

    @staticmethod
    def find_by_id(schedule_id: int) -> Optional[MealSchedule]:
        """
        Find meal schedule by ID
        Equivalent to: mealScheduleRepository.findById(id) in Spring Boot
        """
        try:
            return MealSchedule.objects.select_related('recipe').get(id=schedule_id)
        except MealSchedule.DoesNotExist:
            return None

    @staticmethod
    def save(meal_schedule: MealSchedule) -> MealSchedule:
        """
        Save or update meal schedule
        Equivalent to: mealScheduleRepository.save(mealSchedule) in Spring Boot
        """
        meal_schedule.save()
        return meal_schedule

    @staticmethod
    def delete_by_id(schedule_id: int) -> bool:
        """
        Delete meal schedule by ID
        Equivalent to: mealScheduleRepository.deleteById(id) in Spring Boot
        """
        try:
            meal_schedule = MealSchedule.objects.get(id=schedule_id)
            meal_schedule.delete()
            return True
        except MealSchedule.DoesNotExist:
            return False

    @staticmethod
    def find_by_day_of_week(day: str) -> List[MealSchedule]:
        """
        Find all meals scheduled for a specific day
        Equivalent to: mealScheduleRepository.findByDayOfWeek(day) in Spring Boot
        """
        return list(MealSchedule.objects.filter(day_of_week=day.upper()).select_related('recipe'))

    @staticmethod
    def find_by_meal_type(meal_type: str) -> List[MealSchedule]:
        """
        Find all meals of a specific type (breakfast/lunch/dinner)
        """
        return list(MealSchedule.objects.filter(meal_type=meal_type.upper()).select_related('recipe'))

    @staticmethod
    def find_by_day_and_type(day: str, meal_type: str) -> Optional[MealSchedule]:
        """
        Find meal for a specific day and type
        Useful to check if a meal is already scheduled
        """
        try:
            return MealSchedule.objects.get(
                day_of_week=day.upper(),
                meal_type=meal_type.upper()
            )
        except MealSchedule.DoesNotExist:
            return None

    @staticmethod
    def exists_by_id(schedule_id: int) -> bool:
        """
        Check if meal schedule exists
        """
        return MealSchedule.objects.filter(id=schedule_id).exists()

    @staticmethod
    def get_weekly_schedule() -> List[MealSchedule]:
        """
        Get entire week's meal schedule ordered by day and meal type
        """
        return list(MealSchedule.objects.select_related('recipe').order_by('day_of_week', 'meal_type'))
