from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any


class NutritionInfo(BaseModel):
    """Nutritional information for a recipe."""
    calories: int = Field(..., description="Calorie count")
    protein: str = Field(..., description="Protein amount (e.g., '12g')")
    carbs: str = Field(..., description="Carbohydrate amount (e.g., '60g')")


class Recipe(BaseModel):
    """Recipe model."""
    name: str = Field(..., description="Recipe name")
    ingredients: List[str] = Field(..., description="List of ingredients")
    instructions: List[str] = Field(..., description="Step-by-step instructions")
    cookingTime: str = Field(..., description="Estimated cooking time")
    difficulty: str = Field(..., description="Recipe difficulty (Easy/Medium/Hard)")
    nutrition: NutritionInfo = Field(..., description="Nutritional information")
    
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v not in ['Easy', 'Medium', 'Hard']:
            return 'Easy'  # Default to Easy if invalid
        return v


class RecipeRequest(BaseModel):
    """Request model for recipe analysis."""
    ingredients: str = Field(..., min_length=1, description="Comma-separated list of ingredients")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions (e.g., vegan, gluten-free)")
    
    @validator('ingredients')
    def validate_ingredients(cls, v):
        # Remove extra whitespace and ensure it's not empty
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Ingredients cannot be empty")
        return cleaned


class RecipeResponse(BaseModel):
    """Response model for recipe analysis."""
    recipes: List[Recipe] = Field(..., description="List of generated recipes")
    status: str = Field("success", description="Response status")
    mode: str = Field(..., description="Generation mode (agentic or standard)")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status: str = Field("error", description="Response status")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field("healthy", description="Service status")
    version: str = Field("1.0.0", description="API version")
    mode: str = Field(..., description="Current analyzer mode")