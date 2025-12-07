"""
Recipe Controller
Similar to @RestController in Spring Boot
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services import RecipeService
from serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    RecipeCreateSerializer,
    RecipeUpdateSerializer,
    AddIngredientToRecipeSerializer
)


class RecipeController(APIView):
    """
    REST Controller for Recipe endpoints
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RecipeService()

    def get(self, request, recipe_id=None):
        """
        GET /api/recipes - Get all recipes
        GET /api/recipes/{id} - Get recipe by ID with ingredients

        Similar to @GetMapping in Spring Boot
        """
        try:
            if recipe_id:
                # Get single recipe with ingredients
                recipe_detail = self.service.get_recipe_with_ingredients_detail(recipe_id)
                if not recipe_detail:
                    return Response(
                        {"error": f"Recipe with id {recipe_id} not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                return Response(recipe_detail, status=status.HTTP_200_OK)
            else:
                # Get all recipes
                recipes = self.service.get_all_recipes()
                serializer = RecipeSerializer(recipes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        POST /api/recipes - Create new recipe

        Request body:
        {
            "meal_name": "Chicken Curry",
            "description": "Delicious chicken curry recipe",
            "web_link": "https://example.com/recipe"
        }

        Similar to @PostMapping in Spring Boot
        """
        try:
            serializer = RecipeCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe = self.service.create_recipe(
                meal_name=serializer.validated_data['meal_name'],
                description=serializer.validated_data.get('description'),
                web_link=serializer.validated_data.get('web_link')
            )

            response_serializer = RecipeSerializer(recipe)
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

    def put(self, request, recipe_id):
        """
        PUT /api/recipes/{id} - Update recipe

        Similar to @PutMapping in Spring Boot
        """
        try:
            serializer = RecipeUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe = self.service.update_recipe(
                recipe_id=recipe_id,
                meal_name=serializer.validated_data.get('meal_name'),
                description=serializer.validated_data.get('description'),
                web_link=serializer.validated_data.get('web_link')
            )

            if not recipe:
                return Response(
                    {"error": f"Recipe with id {recipe_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = RecipeSerializer(recipe)
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

    def delete(self, request, recipe_id):
        """
        DELETE /api/recipes/{id} - Delete recipe

        Similar to @DeleteMapping in Spring Boot
        """
        try:
            deleted = self.service.delete_recipe(recipe_id)
            if not deleted:
                return Response(
                    {"error": f"Recipe with id {recipe_id} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {"message": f"Recipe {recipe_id} deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecipeIngredientController(APIView):
    """
    Controller for managing ingredients in a recipe
    POST /api/recipes/{id}/ingredients - Add ingredient to recipe
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RecipeService()

    def post(self, request, recipe_id):
        """
        POST /api/recipes/{id}/ingredients - Add ingredient to recipe

        Request body:
        {
            "ingredient_id": 1,
            "quantity": "2 pieces"
        }
        """
        try:
            serializer = AddIngredientToRecipeSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            recipe_ingredient = self.service.add_ingredient_to_recipe(
                recipe_id=recipe_id,
                ingredient_id=serializer.validated_data['ingredient_id'],
                quantity=serializer.validated_data['quantity']
            )

            return Response(
                {
                    "message": "Ingredient added to recipe successfully",
                    "recipe_id": recipe_ingredient.recipe.id,
                    "ingredient_id": recipe_ingredient.ingredient.id,
                    "quantity": recipe_ingredient.quantity
                },
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


class RecipeSearchController(APIView):
    """
    Search endpoint for recipes
    GET /api/recipes/search?name=curry
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RecipeService()

    def get(self, request):
        """
        Search recipes by meal name
        Query param: name
        """
        try:
            name = request.query_params.get('name', '')
            recipes = self.service.search_recipes_by_name(name)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
