"""
Nutrition calculation tool for recipe analysis.
Provides functions for calculating nutritional information of recipes.
"""

from typing import List, Dict, Any
import json


def calculate_nutrition(ingredients: List[str], servings: int = 4) -> Dict[str, Any]:
    """
    Calculate nutritional information for a list of ingredients.
    
    Args:
        ingredients: List of ingredient names
        servings: Number of servings (default: 4)
        
    Returns:
        Dictionary with nutritional information
    """
    # Basic nutrition database (simplified for demo)
    nutrition_db = {
        # Proteins
        "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15},
        "pork": {"calories": 242, "protein": 27, "carbs": 0, "fat": 14},
        "fish": {"calories": 206, "protein": 22, "carbs": 0, "fat": 12},
        "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
        "tuna": {"calories": 132, "protein": 28, "carbs": 0, "fat": 1},
        "eggs": {"calories": 155, "protein": 13, "carbs": 1, "fat": 11},
        "tofu": {"calories": 76, "protein": 8, "carbs": 2, "fat": 5},
        
        # Grains & Carbs
        "rice": {"calories": 130, "protein": 3, "carbs": 28, "fat": 0.3},
        "pasta": {"calories": 131, "protein": 5, "carbs": 25, "fat": 1.1},
        "bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2},
        "quinoa": {"calories": 222, "protein": 8, "carbs": 39, "fat": 3.6},
        "oats": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7},
        
        # Vegetables
        "tomatoes": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2},
        "onions": {"calories": 40, "protein": 1.1, "carbs": 9.3, "fat": 0.1},
        "garlic": {"calories": 149, "protein": 6.4, "carbs": 33, "fat": 0.5},
        "carrots": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2},
        "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
        "bell peppers": {"calories": 31, "protein": 1, "carbs": 7, "fat": 0.3},
        "mushrooms": {"calories": 22, "protein": 3.1, "carbs": 3.3, "fat": 0.3},
        
        # Dairy
        "cheese": {"calories": 113, "protein": 7, "carbs": 1, "fat": 9},
        "parmesan": {"calories": 110, "protein": 10, "carbs": 1, "fat": 7},
        "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1},
        "butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fat": 81},
        "yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        
        # Oils & Fats
        "olive oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100},
        "coconut oil": {"calories": 862, "protein": 0, "carbs": 0, "fat": 100},
        
        # Herbs & Spices (minimal calories)
        "salt": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0},
        "pepper": {"calories": 251, "protein": 10, "carbs": 64, "fat": 3},
        "basil": {"calories": 22, "protein": 3.2, "carbs": 2.6, "fat": 0.6},
        "oregano": {"calories": 265, "protein": 9, "carbs": 69, "fat": 4.3},
        "thyme": {"calories": 101, "protein": 5.6, "carbs": 24, "fat": 1.7},
        "parsley": {"calories": 36, "protein": 3, "carbs": 6, "fat": 0.8},
    }
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for ingredient in ingredients:
        # Normalize ingredient name
        ingredient_clean = ingredient.lower().strip()
        
        # Try exact match first
        if ingredient_clean in nutrition_db:
            nutrition = nutrition_db[ingredient_clean]
        else:
            # Try partial matches for compound ingredients
            nutrition = None
            for key in nutrition_db:
                if key in ingredient_clean or ingredient_clean in key:
                    nutrition = nutrition_db[key]
                    break
            
            # Default nutrition if not found
            if nutrition is None:
                nutrition = {"calories": 50, "protein": 2, "carbs": 8, "fat": 1}
        
        # Assume 100g serving per ingredient (adjustable)
        total_calories += nutrition["calories"]
        total_protein += nutrition["protein"]
        total_carbs += nutrition["carbs"]
        total_fat += nutrition["fat"]
    
    # Calculate per serving
    per_serving_calories = round(total_calories / servings)
    per_serving_protein = round(total_protein / servings, 1)
    per_serving_carbs = round(total_carbs / servings, 1)
    per_serving_fat = round(total_fat / servings, 1)
    
    return {
        "calories": per_serving_calories,
        "protein": f"{per_serving_protein}g",
        "carbs": f"{per_serving_carbs}g",
        "fat": f"{per_serving_fat}g",
        "servings": servings
    }


def estimate_cooking_time(ingredients: List[str], complexity: str = "medium") -> str:
    """
    Estimate cooking time based on ingredients and complexity.
    
    Args:
        ingredients: List of ingredient names
        complexity: Recipe complexity (easy/medium/hard)
        
    Returns:
        Estimated cooking time string
    """
    # Base times for different ingredient types (in minutes)
    time_map = {
        # Proteins (longest cooking times)
        "chicken": 25, "beef": 30, "pork": 25, "fish": 15, "salmon": 20,
        "tuna": 10, "eggs": 5, "tofu": 10,
        
        # Grains
        "rice": 20, "pasta": 12, "quinoa": 15, "oats": 5,
        
        # Vegetables (quick cooking)
        "tomatoes": 5, "onions": 8, "garlic": 2, "carrots": 10,
        "broccoli": 8, "spinach": 3, "bell peppers": 6, "mushrooms": 5,
        
        # No cooking time
        "cheese": 0, "parmesan": 0, "milk": 0, "butter": 0,
        "olive oil": 0, "salt": 0, "pepper": 0, "herbs": 0,
    }
    
    # Find the longest cooking ingredient
    max_time = 0
    for ingredient in ingredients:
        ingredient_clean = ingredient.lower().strip()
        for key, time in time_map.items():
            if key in ingredient_clean:
                max_time = max(max_time, time)
                break
        else:
            # Default time for unknown ingredients
            max_time = max(max_time, 10)
    
    # Adjust for complexity
    complexity_multiplier = {
        "easy": 1.0,
        "medium": 1.3,
        "hard": 1.8
    }
    
    final_time = int(max_time * complexity_multiplier.get(complexity.lower(), 1.0))
    
    # Add prep time (5-15 minutes based on complexity)
    prep_time = {"easy": 5, "medium": 10, "hard": 15}
    final_time += prep_time.get(complexity.lower(), 10)
    
    return f"{final_time} minutes"


def validate_ingredients(raw_ingredients: str) -> List[str]:
    """
    Validate and clean ingredient list.
    
    Args:
        raw_ingredients: Comma-separated string of ingredients
        
    Returns:
        List of cleaned ingredient names
    """
    if not raw_ingredients or not raw_ingredients.strip():
        return []
    
    # Split by comma and clean each ingredient
    ingredients = []
    for ingredient in raw_ingredients.split(","):
        clean_ingredient = ingredient.strip().lower()
        
        # Remove common cooking terms and measurements
        cleanup_terms = [
            "cup", "cups", "tbsp", "tsp", "tablespoon", "tablespoons", 
            "teaspoon", "teaspoons", "lb", "lbs", "oz", "ounce", "ounces",
            "pound", "pounds", "gram", "grams", "kg", "kilogram", "kilograms",
            "fresh", "dried", "chopped", "diced", "sliced", "minced",
            "large", "small", "medium", "whole", "half", "quarter",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
        ]
        
        words = clean_ingredient.split()
        cleaned_words = []
        
        for word in words:
            # Remove numbers and measurements
            if not any(term in word for term in cleanup_terms):
                cleaned_words.append(word)
        
        if cleaned_words:
            clean_ingredient = " ".join(cleaned_words)
            if clean_ingredient and len(clean_ingredient) > 1:
                ingredients.append(clean_ingredient.title())
    
    return ingredients


def format_recipe_response(recipe_data: Dict[str, Any]) -> str:
    """
    Format recipe data into a structured JSON string.
    
    Args:
        recipe_data: Dictionary containing recipe information
        
    Returns:
        Formatted JSON string
    """
    try:
        return json.dumps(recipe_data, indent=2, ensure_ascii=False)
    except Exception as e:
        return str(recipe_data)