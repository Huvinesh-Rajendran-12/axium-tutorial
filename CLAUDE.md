## Smart Recipe Analyzer Backend Plan with DSPy

### 1. **Project Structure**
```
axium-tutorial/
├── backend/
│   ├── __init__.py
│   ├── app.py              # FastAPI application
│   ├── dspy_modules/
│   │   ├── __init__.py
│   │   ├── recipe_analyzer.py  # DSPy recipe module
│   │   └── signatures.py       # DSPy signatures
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic models
│   ├── tools/
│   │   ├── __init__.py
│   │   └── nutrition_calculator.py
│   └── config.py
├── frontend/               # Frontend implementation
├── tests/
└── requirements.txt
```

### 2. **Backend Implementation Steps**

#### Step 1: Set up Dependencies
- Install FastAPI, DSPy, pydantic, uvicorn
- Configure environment variables for API keys
- Set up DSPy caching

#### Step 2: Define DSPy Signatures
- `IngredientsToRecipes`: ingredients -> recipes with nutrition
- Clear input/output specifications for optimization

#### Step 3: Create DSPy Modules
- Use `dspy.ChainOfThought` for recipe generation
- Implement structured output parsing
- Add validation and error handling

#### Step 4: Build FastAPI Application
- `/api/analyze` endpoint for recipe analysis
- Request validation with Pydantic
- CORS configuration for frontend
- Error handling middleware

#### Step 5: Implement Tools (if needed)
- Nutrition calculation tool
- Ingredient validation tool
- Recipe formatting tool

### 3. **Key DSPy Components**

```python
# Example signature
class RecipeSignature(dspy.Signature):
    """Generate recipes from ingredients with nutritional info."""
    ingredients = dspy.InputField(desc="comma-separated list of ingredients")
    recipes = dspy.OutputField(desc="JSON array of 2-3 recipes with nutrition")

# Recipe analyzer module
class RecipeAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(RecipeSignature)
    
    def forward(self, ingredients):
        # Generate recipes with structured output
        result = self.generate(ingredients=ingredients)
        # Parse and validate JSON response
        return parsed_recipes
```

### 4. **API Design**

**POST /api/analyze**
- Request: `{"ingredients": "pasta, garlic, butter, parmesan"}`
- Response: JSON with 2-3 recipes including:
  - Recipe name
  - Ingredients list
  - Step-by-step instructions
  - Cooking time & difficulty
  - Nutritional information

### 5. **DSPy Optimization Strategy**
1. Start with zero-shot `dspy.ChainOfThought`
2. Create training examples with diverse ingredients
3. Use `BootstrapFewShot` optimizer for prompt tuning
4. Save optimized module for production use

### 6. **Implementation Order**
1. Set up project structure and dependencies
2. Create basic FastAPI app with health check
3. Implement DSPy signatures and modules
4. Build recipe analysis endpoint
5. Add error handling and validation
6. Create optimization script with examples
7. Test with various ingredient combinations
8. Document API and deployment instructions

### 7. **Bonus Features Architecture**
- **Dietary Restrictions**: Add filter parameter to signature
- **Recipe Rating**: Store ratings in memory/database
- **Substitutions**: Create separate DSPy module
- **History**: Add in-memory cache
- **Images**: Integrate DALL-E API call

This approach leverages DSPy's strengths for structured output generation while maintaining clean separation of concerns and following the framework's best practices.