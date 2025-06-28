# Smart Recipe Analyzer Backend

This is the backend API for the Smart Recipe Analyzer application, built with FastAPI and DSPy.

## Features

- Generate 2-3 recipe suggestions from a list of ingredients
- Provide nutritional information for each recipe
- Support for dietary restrictions (bonus feature)
- Built with DSPy for optimized prompt engineering
- RESTful API with automatic documentation

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or if using uv:
   uv pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your LLM API key (OpenAI or Anthropic).

3. **Run the server:**
   ```bash
   python run_backend.py
   # or
   python -m backend.app
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/analyze` - Analyze ingredients and generate recipes
- `GET /api/example` - Get example response
- `GET /docs` - Interactive API documentation

## API Usage

### Analyze Ingredients

**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": "pasta, garlic, butter, parmesan",
    "dietary_restrictions": "vegetarian"
  }'
```

**Response:**
```json
{
  "recipes": [
    {
      "name": "Garlic Butter Pasta",
      "ingredients": ["pasta", "garlic", "butter", "parmesan"],
      "instructions": ["Boil pasta...", "Sauté garlic..."],
      "cookingTime": "20 minutes",
      "difficulty": "Easy",
      "nutrition": {
        "calories": 450,
        "protein": "12g",
        "carbs": "60g"
      }
    }
  ],
  "status": "success"
}
```

## DSPy Architecture

The backend uses DSPy modules for:
1. **Ingredient Validation**: Cleans and validates user input
2. **Recipe Generation**: Uses ChainOfThought for structured recipe generation
3. **Recipe Enhancement**: Applies dietary restrictions if specified

## Development

- The DSPy cache is stored in `.dspy_cache/` to improve performance
- Logs are available in the console when running with `DEBUG=True`
- API documentation is auto-generated at `/docs`