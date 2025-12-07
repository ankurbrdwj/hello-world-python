"""
MealSchedule Controller
Similar to @RestController in Spring Boot
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services import MealScheduleService
from serializers import (
    MealScheduleSerializer,
    MealScheduleCreateSerializer,
    MealScheduleUpdateSerializer
)


class MealScheduleController(APIView):
    """
    REST Controller for MealSchedule endpoints
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MealScheduleService()

    def get(self, request, schedule_id=None):
        """
        GET /api/meal-schedule - Get all schedules
        GET /api/meal-schedule/{id} - Get schedule by ID
        GET /api/meal-schedule?day=MONDAY - Filter by day
        GET /api/meal-schedule?type=BREAKFAST - Filter by meal type

        Similar to @GetMapping in Spring Boot
        """
        try:
            if schedule_id:
                # Get single schedule
                schedule = self.service.get_schedule_by_id(schedule_id)
                if not schedule:
                    return Response(
                        {"error": f"Meal schedule with id {schedule_id} not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                serializer = MealScheduleSerializer(schedule)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Get schedules with optional filters
                day = request.query_params.get('day')
                meal_type = request.query_params.get('type')

                if day:
                    schedules = self.service.get_schedules_by_day(day)
                elif meal_type:
                    schedules = self.service.get_schedules_by_meal_type(meal_type)
                else:
                    schedules = self.service.get_weekly_schedule()

                serializer = MealScheduleSerializer(schedules, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        POST /api/meal-schedule - Schedule a new meal

        Request body:
        {
            "meal_name": "Chicken Curry",
            "day_of_week": "MONDAY",
            "meal_type": "LUNCH",
            "recipe_id": 1,  // optional
            "notes": "Extra spicy"  // optional
        }

        Similar to @PostMapping in Spring Boot
        """
        try:
            serializer = MealScheduleCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            schedule = self.service.schedule_meal(
                meal_name=serializer.validated_data['meal_name'],
                day_of_week=serializer.validated_data['day_of_week'],
                meal_type=serializer.validated_data['meal_type'],
                recipe_id=serializer.validated_data.get('recipe_id'),
                notes=serializer.validated_data.get('notes')
            )

            response_serializer = MealScheduleSerializer(schedule)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, schedule_id):
        """
        PUT /api/meal-schedule/{id} - Update meal schedule

        Similar to @PutMapping in Spring Boot
        """
        try:
            serializer = MealScheduleUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            schedule = self.service.update_schedule(
                schedule_id=schedule_id,
                meal_name=serializer.validated_data.get('meal_name'),
                day_of_week=serializer.validated_data.get('day_of_week'),
                meal_type=serializer.validated_data.get('meal_type'),
                recipe_id=serializer.validated_data.get('recipe_id'),
                notes=serializer.validated_data.get('notes')
            )

            if not schedule:
                return Response(
                    {"error": f"Meal schedule with id {schedule_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = MealScheduleSerializer(schedule)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, schedule_id):
        """
        DELETE /api/meal-schedule/{id} - Delete meal schedule

        Similar to @DeleteMapping in Spring Boot
        """
        try:
            deleted = self.service.delete_schedule(schedule_id)
            if not deleted:
                return Response(
                    {"error": f"Meal schedule with id {schedule_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"message": f"Meal schedule {schedule_id} deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
