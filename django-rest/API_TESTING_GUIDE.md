# API Testing Guide

## Start the Server

```bash
python3 manage.py runserver
```

The server will be available at: http://127.0.0.1:8000/

---

## Ingredients API

### 1. Get All Ingredients
```bash
curl -X GET http://127.0.0.1:8000/api/ingredients/
```

### 2. Get Ingredients in Stock Only
```bash
curl -X GET http://127.0.0.1:8000/api/ingredients/?in_stock=true
```

### 3. Get Ingredient by ID
```bash
curl -X GET http://127.0.0.1:8000/api/ingredients/1/
```

### 4. Create Ingredient
```bash
curl -X POST http://127.0.0.1:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomato",
    "units_available": 10,
    "unit_type": "pieces"
  }'
```

### 5. Update Ingredient
```bash
curl -X PUT http://127.0.0.1:8000/api/ingredients/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "units_available": 15
  }'
```

### 6. Delete Ingredient
```bash
curl -X DELETE http://127.0.0.1:8000/api/ingredients/1/
```

### 7. Search Ingredients by Name
```bash
curl -X GET "http://127.0.0.1:8000/api/ingredients/search/?name=tomato"
```

---

## Recipes API

### 1. Get All Recipes
```bash
curl -X GET http://127.0.0.1:8000/api/recipes/
```

### 2. Get Recipe by ID (with ingredients)
```bash
curl -X GET http://127.0.0.1:8000/api/recipes/1/
```

**Response Example:**
```json
{
  "id": 1,
  "meal_name": "Chicken Curry",
  "description": "Delicious Indian curry",
  "web_link": "https://example.com/recipe",
  "ingredients": [
    {
      "ingredient_id": 3,
      "ingredient_name": "Chicken",
      "quantity": "500g",
      "unit_type": "kg"
    },
    {
      "ingredient_id": 2,
      "ingredient_name": "Rice",
      "quantity": "200g",
      "unit_type": "kg"
    }
  ]
}
```

### 3. Create Recipe
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "description": "Delicious Indian curry",
    "web_link": "https://example.com/recipe"
  }'
```

### 4. Add Ingredient to Recipe
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/1/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{
    "ingredient_id": 3,
    "quantity": "500g"
  }'
```

### 5. Update Recipe
```bash
curl -X PUT http://127.0.0.1:8000/api/recipes/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

### 6. Delete Recipe
```bash
curl -X DELETE http://127.0.0.1:8000/api/recipes/1/
```

### 7. Search Recipes by Name
```bash
curl -X GET "http://127.0.0.1:8000/api/recipes/search/?name=curry"
```

---

## Meal Schedule API

### 1. Get Weekly Meal Schedule
```bash
curl -X GET http://127.0.0.1:8000/api/meal-schedule/
```

### 2. Get Meals for Specific Day
```bash
curl -X GET "http://127.0.0.1:8000/api/meal-schedule/?day=MONDAY"
```

Valid days: `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`

### 3. Get Meals by Type
```bash
curl -X GET "http://127.0.0.1:8000/api/meal-schedule/?type=BREAKFAST"
```

Valid types: `BREAKFAST`, `LUNCH`, `DINNER`

### 4. Get Schedule by ID
```bash
curl -X GET http://127.0.0.1:8000/api/meal-schedule/1/
```

### 5. Schedule a Meal
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

**Note:** `recipe_id` and `notes` are optional

### 6. Update Meal Schedule
```bash
curl -X PUT http://127.0.0.1:8000/api/meal-schedule/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Medium spicy"
  }'
```

### 7. Delete Meal Schedule
```bash
curl -X DELETE http://127.0.0.1:8000/api/meal-schedule/1/
```

---

## Complete Workflow Example

### Step 1: Create Ingredients
```bash
# Create Tomato
curl -X POST http://127.0.0.1:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Tomato", "units_available": 10, "unit_type": "pieces"}'

# Create Rice
curl -X POST http://127.0.0.1:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Rice", "units_available": 5, "unit_type": "kg"}'

# Create Chicken
curl -X POST http://127.0.0.1:8000/api/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Chicken", "units_available": 2, "unit_type": "kg"}'
```

### Step 2: Create a Recipe
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "description": "Delicious Indian curry with rice",
    "web_link": "https://example.com/chicken-curry"
  }'
```

### Step 3: Add Ingredients to Recipe
```bash
# Add Chicken
curl -X POST http://127.0.0.1:8000/api/recipes/1/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"ingredient_id": 3, "quantity": "500g"}'

# Add Rice
curl -X POST http://127.0.0.1:8000/api/recipes/1/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"ingredient_id": 2, "quantity": "200g"}'

# Add Tomato
curl -X POST http://127.0.0.1:8000/api/recipes/1/ingredients/ \
  -H "Content-Type: application/json" \
  -d '{"ingredient_id": 1, "quantity": "2 pieces"}'
```

### Step 4: Schedule the Meal for the Week
```bash
# Monday Lunch
curl -X POST http://127.0.0.1:8000/api/meal-schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "day_of_week": "MONDAY",
    "meal_type": "LUNCH",
    "recipe_id": 1,
    "notes": "First curry of the week"
  }'

# Friday Dinner
curl -X POST http://127.0.0.1:8000/api/meal-schedule/ \
  -H "Content-Type: application/json" \
  -d '{
    "meal_name": "Chicken Curry",
    "day_of_week": "FRIDAY",
    "meal_type": "DINNER",
    "recipe_id": 1
  }'
```

### Step 5: View Your Week's Schedule
```bash
curl -X GET http://127.0.0.1:8000/api/meal-schedule/
```

### Step 6: Check What Ingredients Are in Stock
```bash
curl -X GET http://127.0.0.1:8000/api/ingredients/
```

---

## Using Postman or Browser

You can also test these APIs using:
- **Postman**: Import the endpoints above
- **Browser**: Navigate to http://127.0.0.1:8000/api/ingredients/ for GET requests
- **Django Admin**: http://127.0.0.1:8000/admin/ (after creating superuser)

### Create Superuser (for Admin Panel)
```bash
python3 manage.py createsuperuser
```

Then visit: http://127.0.0.1:8000/admin/
