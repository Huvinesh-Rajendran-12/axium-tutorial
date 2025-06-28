import dspy


class RecipeGenerationSignature(dspy.Signature):
    """Generate recipes from a list of ingredients with nutritional information."""
    
    ingredients = dspy.InputField(
        desc="Comma-separated list of available ingredients"
    )
    
    recipes = dspy.OutputField(
        desc="""JSON array of 2-3 recipes. Each recipe must include:
        - name: Recipe name
        - ingredients: List of ingredients used
        - instructions: List of step-by-step instructions
        - cookingTime: Estimated time (e.g., "20 minutes")
        - difficulty: Easy/Medium/Hard
        - nutrition: Object with calories (number), protein (string), carbs (string)
        
        Format as valid JSON that can be parsed."""
    )


class IngredientValidationSignature(dspy.Signature):
    """Validate and normalize ingredient list."""
    
    raw_ingredients = dspy.InputField(
        desc="Raw comma-separated ingredient list from user"
    )
    
    validated_ingredients = dspy.OutputField(
        desc="Cleaned, validated comma-separated ingredient list"
    )


class RecipeEnhancementSignature(dspy.Signature):
    """Enhance recipe with additional details or substitutions."""
    
    recipe = dspy.InputField(
        desc="Original recipe JSON"
    )
    dietary_restrictions = dspy.InputField(
        desc="Optional dietary restrictions (e.g., vegan, gluten-free)"
    )
    
    enhanced_recipe = dspy.OutputField(
        desc="Enhanced recipe with substitutions if needed"
    )