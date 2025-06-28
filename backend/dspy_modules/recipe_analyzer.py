import json
import dspy
from typing import List, Dict, Any, Optional
from .signatures import (
    RecipeGenerationSignature,
    IngredientValidationSignature,
    RecipeEnhancementSignature
)


class RecipeAnalyzer(dspy.Module):
    """Main DSPy module for analyzing ingredients and generating recipes."""
    
    def __init__(self):
        super().__init__()
        self.validate_ingredients = dspy.ChainOfThought(IngredientValidationSignature)
        self.generate_recipes = dspy.ChainOfThought(RecipeGenerationSignature)
        self.enhance_recipe = dspy.ChainOfThought(RecipeEnhancementSignature)
    
    def forward(self, ingredients: str, dietary_restrictions: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate recipes from ingredients.
        
        Args:
            ingredients: Comma-separated list of ingredients
            dietary_restrictions: Optional dietary restrictions
            
        Returns:
            List of recipe dictionaries
        """
        # Step 1: Validate and normalize ingredients
        validated = self.validate_ingredients(raw_ingredients=ingredients)
        clean_ingredients = validated.validated_ingredients
        
        # Step 2: Generate recipes
        result = self.generate_recipes(ingredients=clean_ingredients)
        
        # Step 3: Parse JSON response
        try:
            recipes_json = self._extract_json(result.recipes)
            recipes = json.loads(recipes_json)
            
            # Ensure we have a list of recipes
            if isinstance(recipes, dict) and "recipes" in recipes:
                recipes = recipes["recipes"]
            elif not isinstance(recipes, list):
                recipes = [recipes]
            
            # Step 4: Enhance recipes if dietary restrictions are specified
            if dietary_restrictions:
                enhanced_recipes = []
                for recipe in recipes:
                    enhanced = self.enhance_recipe(
                        recipe=json.dumps(recipe),
                        dietary_restrictions=dietary_restrictions
                    )
                    try:
                        enhanced_recipe = json.loads(self._extract_json(enhanced.enhanced_recipe))
                        enhanced_recipes.append(enhanced_recipe)
                    except:
                        enhanced_recipes.append(recipe)
                recipes = enhanced_recipes
            
            return recipes[:3]  # Return maximum 3 recipes
            
        except json.JSONDecodeError as e:
            # Fallback: return a simple recipe structure
            return [{
                "name": "Simple Recipe",
                "ingredients": clean_ingredients.split(", "),
                "instructions": ["Combine ingredients and cook as desired"],
                "cookingTime": "30 minutes",
                "difficulty": "Easy",
                "nutrition": {
                    "calories": 300,
                    "protein": "10g",
                    "carbs": "40g"
                }
            }]
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might contain additional content."""
        # Find JSON array or object
        text = text.strip()
        
        # Look for JSON array
        if "[" in text:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                return text[start:end]
        
        # Look for JSON object
        if "{" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return text[start:end]
        
        return text


class SimpleRecipeGenerator(dspy.Module):
    """Simplified recipe generator for testing and fallback."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.Predict(RecipeGenerationSignature)
    
    def forward(self, ingredients: str, dietary_restrictions: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate recipes with basic prediction."""
        try:
            # Single LLM call for faster response
            result = self.generate(ingredients=ingredients)
            
            # Try to parse the JSON response
            recipes_text = result.recipes
            if isinstance(recipes_text, str):
                # Extract JSON from the response
                recipes_json = self._extract_json(recipes_text)
                recipes = json.loads(recipes_json)
                
                if isinstance(recipes, dict) and "recipes" in recipes:
                    recipes = recipes["recipes"]
                elif not isinstance(recipes, list):
                    recipes = [recipes]
                    
                return recipes[:3]
        except Exception as e:
            print(f"Error generating recipes: {e}")
        
        # Quick fallback response
        ingredient_list = [ing.strip() for ing in ingredients.split(",")]
        return [{
            "name": f"Simple {ingredient_list[0].title()} Dish",
            "ingredients": ingredient_list,
            "instructions": [
                "Prepare all ingredients",
                "Cook according to preference",
                "Season to taste and serve"
            ],
            "cookingTime": "20 minutes",
            "difficulty": "Easy",
            "nutrition": {
                "calories": 300,
                "protein": "10g",
                "carbs": "35g"
            }
        }]
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text."""
        text = text.strip()
        
        # Look for JSON array
        if "[" in text:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                return text[start:end]
        
        # Look for JSON object
        if "{" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return text[start:end]
        
        return text