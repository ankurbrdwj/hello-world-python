# Meal Planning REST API

A Django REST API for meal planning, built with Spring Boot-like architecture.

## Architecture

This project mimics Spring Boot's layered architecture:

```
meal-app/
├── entities/          # @Entity classes (JPA entities in Spring Boot)
│   ├── ingredient.py
│   ├── recipe.py
│   └── meal_schedule.py
├── repositories/      # @Repository (JpaRepository in Spring Boot)
│   ├── ingredient_repository.py
│   ├── recipe_repository.py
│   └── meal_schedule_repository.py
├── services/          # @Service (Business logic in Spring Boot)
│   ├── ingredient_service.py
│   ├── recipe_service.py
│   └── meal_schedule_service.py
├── controllers/       # @RestController (REST endpoints in Spring Boot)
│   ├── ingredient_controller.py
│   ├── recipe_controller.py
│   └── meal_schedule_controller.py
├── serializers/       # DTOs (Data Transfer Objects in Spring Boot)
│   ├── ingredient_serializer.py
│   ├── recipe_serializer.py
│   └── meal_schedule_serializer.py
├── config/            # Configuration (application.properties in Spring Boot)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py          # Main application (similar to @SpringBootApplication)
```

## Setup & Run

### 1. Create and run database migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 2. Create a superuser (optional, for admin panel)
```bash
python3 manage.py createsuperuser
```

### 3. Run the development server
```bash
python3 manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## API Endpoints

### Ingredients API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ingredients/` | Get all ingredients |
| GET | `/api/ingredients/?in_stock=true` | Get ingredients in stock |
| GET | `/api/ingredients/{id}/` | Get ingredient by ID |
| POST | `/api/ingredients/` | Create new ingredient |
| PUT | `/api/ingredients/{id}/` | Update ingredient |
| DELETE | `/api/ingredients/{id}/` | Delete ingredient |
| GET | `/api/ingredients/search/?name=tomato` | Search ingredients by name |

### Recipes API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recipes/` | Get all recipes |
| GET | `/api/recipes/{id}/` | Get recipe with ingredients |
| POST | `/api/recipes/` | Create new recipe |
| PUT | `/api/recipes/{id}/` | Update recipe |
| DELETE | `/api/recipes/{id}/` | Delete recipe |
| POST | `/api/recipes/{id}/ingredients/` | Add ingredient to recipe |
| GET | `/api/recipes/search/?name=curry` | Search recipes by name |

### Meal Schedule API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/meal-schedule/` | Get weekly meal schedule |
| GET | `/api/meal-schedule/?day=MONDAY` | Get meals for specific day |
| GET | `/api/meal-schedule/?type=BREAKFAST` | Get meals by type |
| GET | `/api/meal-schedule/{id}/` | Get schedule by ID |
| POST | `/api/meal-schedule/` | Schedule a new meal |
| PUT | `/api/meal-schedule/{id}/` | Update meal schedule |
| DELETE | `/api/meal-schedule/{id}/` | Delete meal schedule |

## Example API Calls

### Create an ingredient
```bash
curl -X POST http://127.0.0.1:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomato",
    "units_available": 10,
    "unit_type": "pieces"
  }'
```

### Create a recipe
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "description": "Delicious Indian curry",
    "web_link": "https://example.com/recipe"
  }'
```

### Add ingredient to recipe
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/1/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{
    "ingredient_id": 1,
    "quantity": "2 pieces"
  }'
```

### Schedule a meal
```bash
curl -X POST http://127.0.0.1:8000/api/meal-schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "day_of_week": "MONDAY",
    "meal_type": "LUNCH",
    "recipe_id": 1,
    "notes": "Extra spicy"
  }'
```

## Python/Django vs Java/Spring Boot Comparison

| Spring Boot | Django | Notes |
|-------------|--------|-------|
| `@Entity` | `models.Model` | Database entities |
| `@Repository` / `JpaRepository` | Custom repository classes | Data access layer |
| `@Service` | Service classes | Business logic |
| `@RestController` | `APIView` | REST controllers |
| DTO classes | `Serializer` | Request/response mapping |
| `application.properties` | `settings.py` | Configuration |
| `@Autowired` | Manual instantiation | Dependency injection |
| `@GetMapping`, `@PostMapping` | `def get()`, `def post()` | HTTP methods |
| `ResponseEntity<T>` | `Response()` | HTTP responses |
| JPA Relationships | Django ORM | Database relationships |

## Key Python/Django Concepts for Java Developers

1. **No Annotations**: Python uses class inheritance and method names instead of annotations
2. **Duck Typing**: No need to declare types (though you can use type hints)
3. **ORM**: Django ORM is similar to JPA but more Pythonic
4. **Settings**: All configuration in `settings.py` instead of `.properties` files
5. **Migration System**: Similar to Flyway/Liquibase but built-in
6. **Admin Panel**: Auto-generated admin interface (bonus!)

## Django Admin Panel

Visit http://127.0.0.1:8000/admin/ to access the Django admin panel.
You can manage all entities through a web interface!
