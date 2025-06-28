from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from .config import (
    API_VERSION, API_TITLE, API_DESCRIPTION,
    ALLOWED_ORIGINS, init_dspy, DEBUG
)
from .models.schemas import (
    RecipeRequest, RecipeResponse, ErrorResponse, 
    HealthCheckResponse, Recipe
)
from .dspy_modules.recipe_analyzer import RecipeAnalyzer, SimpleRecipeGenerator

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variable for the recipe analyzer
recipe_analyzer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown."""
    global recipe_analyzer
    
    try:
        # Initialize DSPy
        logger.info("Initializing DSPy...")
        init_dspy()
        
        # Initialize recipe analyzer
        logger.info("Initializing Recipe Analyzer...")
        # Use SimpleRecipeGenerator for faster responses
        recipe_analyzer = SimpleRecipeGenerator()
        
        logger.info("Application startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise
    finally:
        logger.info("Application shutdown")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status="error"
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if DEBUG else None,
            status="error"
        ).dict()
    )


# Routes
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Smart Recipe Analyzer API",
        "version": API_VERSION,
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=API_VERSION
    )


@app.post("/api/analyze", response_model=RecipeResponse)
async def analyze_ingredients(request: RecipeRequest):
    """
    Analyze ingredients and generate recipes with nutritional information.
    
    Args:
        request: RecipeRequest with ingredients and optional dietary restrictions
        
    Returns:
        RecipeResponse with generated recipes
    """
    global recipe_analyzer
    
    if not recipe_analyzer:
        raise HTTPException(
            status_code=503,
            detail="Recipe analyzer is not initialized"
        )
    
    try:
        logger.info(f"Analyzing ingredients: {request.ingredients}")
        
        # Generate recipes using DSPy
        recipes = recipe_analyzer(
            ingredients=request.ingredients,
            dietary_restrictions=request.dietary_restrictions
        )
        
        # Validate and format recipes
        validated_recipes = []
        for recipe_data in recipes:
            try:
                # Create Recipe model instance for validation
                recipe = Recipe(**recipe_data)
                validated_recipes.append(recipe)
            except Exception as e:
                logger.warning(f"Failed to validate recipe: {str(e)}")
                # Skip invalid recipes
                continue
        
        if not validated_recipes:
            # Fallback if no valid recipes
            validated_recipes = [
                Recipe(
                    name="Simple Dish",
                    ingredients=request.ingredients.split(", "),
                    instructions=["Prepare ingredients", "Cook as desired"],
                    cookingTime="30 minutes",
                    difficulty="Easy",
                    nutrition={
                        "calories": 300,
                        "protein": "10g",
                        "carbs": "40g"
                    }
                )
            ]
        
        return RecipeResponse(
            recipes=validated_recipes,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"Failed to analyze ingredients: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recipes: {str(e)}"
        )


@app.get("/api/example", response_model=RecipeResponse)
async def get_example():
    """Get an example response for testing."""
    return RecipeResponse(
        recipes=[
            Recipe(
                name="Garlic Butter Pasta",
                ingredients=["pasta", "garlic", "butter", "parmesan cheese", "black pepper"],
                instructions=[
                    "Boil pasta according to package directions",
                    "Mince garlic and saute in butter until fragrant",
                    "Toss cooked pasta with garlic butter",
                    "Add grated parmesan and black pepper to taste"
                ],
                cookingTime="20 minutes",
                difficulty="Easy",
                nutrition={
                    "calories": 450,
                    "protein": "12g",
                    "carbs": "60g"
                }
            ),
            Recipe(
                name="Simple Aglio e Olio",
                ingredients=["pasta", "garlic", "olive oil", "red pepper flakes", "parsley"],
                instructions=[
                    "Cook pasta until al dente",
                    "Slice garlic and cook in olive oil",
                    "Add red pepper flakes",
                    "Toss pasta with garlic oil and parsley"
                ],
                cookingTime="15 minutes",
                difficulty="Easy",
                nutrition={
                    "calories": 380,
                    "protein": "10g",
                    "carbs": "55g"
                }
            )
        ],
        status="success"
    )


if __name__ == "__main__":
    import uvicorn
    from .config import HOST, PORT
    
    uvicorn.run(
        "backend.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )