"""
Agentic Recipe Analyzer using DSPy modules with tools.
"""

import json
import dspy
from typing import List, Dict, Any, Optional

from ..tools.nutrition_calculator import (
    calculate_nutrition, 
    estimate_cooking_time, 
    validate_ingredients,
    format_recipe_response
)


class SimpleAgenticAnalyzer(dspy.Module):
    """
    Simplified agentic analyzer that uses individual tool calls.
    More reliable than full ReAct for this use case.
    """
    
    def __init__(self):
        super().__init__()
        self.recipe_generator = dspy.ChainOfThought("ingredients, constraints -> recipe_ideas")
        self.instruction_generator = dspy.Predict("recipe_name, ingredients -> detailed_instructions")
    
    def forward(self, ingredients: str, dietary_restrictions: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate recipes using simplified agentic approach."""
        try:
            # Step 1: Validate ingredients using tool
            cleaned_ingredients = validate_ingredients(ingredients)
            if not cleaned_ingredients:
                cleaned_ingredients = [ing.strip() for ing in ingredients.split(",")]
            
            # Step 2: Generate recipe ideas
            constraints = f"dietary restrictions: {dietary_restrictions}" if dietary_restrictions else "no constraints"
            ideas_result = self.recipe_generator(
                ingredients=", ".join(cleaned_ingredients),
                constraints=constraints
            )
            
            # Step 3: Create structured recipes
            recipes = []
            
            for i, recipe_concept in enumerate(["classic", "gourmet", "quick"], 1):
                # Generate recipe name and instructions
                recipe_name = f"{recipe_concept.title()} {cleaned_ingredients[0]} Recipe"
                
                instructions_result = self.instruction_generator(
                    recipe_name=recipe_name,
                    ingredients=", ".join(cleaned_ingredients)
                )
                
                # Use tools to get nutrition and timing
                nutrition = calculate_nutrition(cleaned_ingredients)
                cooking_time = estimate_cooking_time(
                    cleaned_ingredients, 
                    "easy" if recipe_concept == "quick" else "medium"
                )
                
                # Parse instructions from LLM output
                instructions = self._parse_instructions(instructions_result.detailed_instructions)
                
                recipe = {
                    "name": recipe_name,
                    "ingredients": cleaned_ingredients,
                    "instructions": instructions,
                    "cookingTime": cooking_time,
                    "difficulty": "Easy" if recipe_concept == "quick" else "Medium",
                    "nutrition": {
                        "calories": nutrition["calories"],
                        "protein": nutrition["protein"],
                        "carbs": nutrition["carbs"]
                    }
                }
                recipes.append(recipe)
            
            return recipes[:3]  # Return max 3 recipes
            
        except Exception as e:
            print(f"Error in simplified agentic analysis: {e}")
            # Final fallback
            return self._basic_fallback(ingredients)
    
    def _parse_instructions(self, raw_instructions: str) -> List[str]:
        """Parse instructions from LLM output into a list."""
        if not raw_instructions:
            return ["Prepare ingredients and cook as desired"]
        
        # Split by common delimiters
        instructions = []
        lines = raw_instructions.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:  # Filter out very short lines
                # Remove numbering if present
                if line[0].isdigit() and '.' in line[:3]:
                    line = line.split('.', 1)[1].strip()
                instructions.append(line)
        
        if not instructions:
            # Split by periods as fallback
            sentences = raw_instructions.split('.')
            instructions = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        return instructions[:6]  # Max 6 instructions
    
    def _basic_fallback(self, ingredients: str) -> List[Dict[str, Any]]:
        """Basic fallback if everything fails."""
        ingredient_list = [ing.strip() for ing in ingredients.split(",")]
        nutrition = calculate_nutrition(ingredient_list)
        
        return [{
            "name": f"Simple {ingredient_list[0]} Dish",
            "ingredients": ingredient_list,
            "instructions": [
                "Prepare all ingredients",
                "Cook ingredients together",
                "Season to taste",
                "Serve when ready"
            ],
            "cookingTime": "25 minutes",
            "difficulty": "Easy",
            "nutrition": {
                "calories": nutrition["calories"],
                "protein": nutrition["protein"],
                "carbs": nutrition["carbs"]
            }
        }]