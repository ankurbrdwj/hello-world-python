"""
Ingredient Controller
Similar to @RestController in Spring Boot

In Spring Boot:
@RestController
@RequestMapping("/api/ingredients")
public class IngredientController {
    @Autowired
    private IngredientService ingredientService;

    @GetMapping
    public List<Ingredient> getAllIngredients() {
        return ingredientService.getAllIngredients();
    }
}

In Django REST Framework, we use APIView or ViewSets
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services import IngredientService
from serializers import (
    IngredientSerializer,
    IngredientCreateSerializer,
    IngredientUpdateSerializer
)


class IngredientController(APIView):
    """
    REST Controller for Ingredient endpoints
    Similar to @RestController in Spring Boot
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = IngredientService()

    def get(self, request, ingredient_id=None):
        """
        GET /api/ingredients - Get all ingredients
        GET /api/ingredients/{id} - Get ingredient by ID

        Similar to @GetMapping in Spring Boot
        """
        try:
            if ingredient_id:
                # Get single ingredient
                ingredient = self.service.get_ingredient_by_id(ingredient_id)
                if not ingredient:
                    return Response(
                        {"error": f"Ingredient with id {ingredient_id} not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                serializer = IngredientSerializer(ingredient)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Get all ingredients or filter by stock
                in_stock_only = request.query_params.get('in_stock', 'false').lower() == 'true'

                if in_stock_only:
                    ingredients = self.service.get_ingredients_in_stock()
                else:
                    ingredients = self.service.get_all_ingredients()

                serializer = IngredientSerializer(ingredients, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        POST /api/ingredients - Create new ingredient

        Request body:
        {
            "name": "Tomato",
            "units_available": 5.0,
            "unit_type": "kg"
        }

        Similar to @PostMapping in Spring Boot
        """
        try:
            serializer = IngredientCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            ingredient = self.service.create_ingredient(
                name=serializer.validated_data['name'],
                units_available=serializer.validated_data['units_available'],
                unit_type=serializer.validated_data.get('unit_type', 'pieces')
            )

            response_serializer = IngredientSerializer(ingredient)
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

    def put(self, request, ingredient_id):
        """
        PUT /api/ingredients/{id} - Update ingredient

        Similar to @PutMapping in Spring Boot
        """
        try:
            serializer = IngredientUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            ingredient = self.service.update_ingredient(
                ingredient_id=ingredient_id,
                name=serializer.validated_data.get('name'),
                units_available=serializer.validated_data.get('units_available'),
                unit_type=serializer.validated_data.get('unit_type')
            )

            if not ingredient:
                return Response(
                    {"error": f"Ingredient with id {ingredient_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = IngredientSerializer(ingredient)
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

    def delete(self, request, ingredient_id):
        """
        DELETE /api/ingredients/{id} - Delete ingredient

        Similar to @DeleteMapping in Spring Boot
        """
        try:
            deleted = self.service.delete_ingredient(ingredient_id)
            if not deleted:
                return Response(
                    {"error": f"Ingredient with id {ingredient_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"message": f"Ingredient {ingredient_id} deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IngredientSearchController(APIView):
    """
    Search endpoint for ingredients
    GET /api/ingredients/search?name=tomato
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = IngredientService()

    def get(self, request):
        """
        Search ingredients by name
        Query param: name
        """
        try:
            name = request.query_params.get('name', '')
            ingredients = self.service.search_ingredients_by_name(name)
            serializer = IngredientSerializer(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
