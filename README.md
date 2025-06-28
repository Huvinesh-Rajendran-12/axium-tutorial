# Smart Recipe Analyzer

An AI-powered web application that generates recipe suggestions with nutritional analysis from a list of ingredients. Built with FastAPI, DSPy, and modern web technologies.

## Overview

Smart Recipe Analyzer uses advanced AI (via DSPy framework) to:
- Generate 2-3 recipe suggestions from your available ingredients
- Provide detailed cooking instructions
- Calculate nutritional information
- Support dietary restrictions (bonus feature)
- Offer a clean, responsive web interface

## Features

### Core Features
- **Ingredient Input**: Simple comma-separated ingredient list
- **Recipe Generation**: AI-powered recipe creation with structured output
- **Nutritional Analysis**: Calories, protein, and carbohydrate information
- **Difficulty Levels**: Easy, Medium, or Hard classifications
- **Cooking Time Estimates**: Realistic time requirements

### Technical Features
- **DSPy Integration**: Optimized prompt engineering without manual tuning
- **FastAPI Backend**: High-performance async API
- **Structured Output**: Consistent JSON responses
- **Error Handling**: Graceful fallbacks and user-friendly messages
- **API Documentation**: Auto-generated interactive docs

## Tech Stack

### Backend
- **Framework**: FastAPI
- **AI/ML**: DSPy (Stanford's prompt optimization framework)
- **Language Model**: Supports OpenAI, Anthropic, or custom LLMs
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend (Planned)
- React/Vue.js or Vanilla JavaScript
- Responsive design
- Real-time loading states

## Installation

### Prerequisites
- Python 3.13+
- API key for your chosen LLM (OpenAI, Anthropic, etc.)
- uv (recommended) or pip

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-recipe-analyzer.git
   cd smart-recipe-analyzer
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API credentials:
   ```env
   # For OpenAI
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-3.5-turbo
   LLM_API_KEY=your-openai-api-key
   
   # For Anthropic
   LLM_PROVIDER=anthropic
   LLM_MODEL=claude-3-sonnet-20240229
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

4. **Run the server**
   ```bash
   python run_backend.py
   # Or
   uv run run_backend.py
   ```

   The API will be available at `http://localhost:8000`

## API Usage

### Interactive Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

### Endpoints

#### Generate Recipes
```bash
POST /api/analyze

curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": "chicken, rice, tomatoes, onions, garlic",
    "dietary_restrictions": "gluten-free"
  }'
```

**Response:**
```json
{
  "recipes": [
    {
      "name": "Spanish Chicken and Rice",
      "ingredients": ["chicken", "rice", "tomatoes", "onions", "garlic"],
      "instructions": [
        "Season chicken with salt and pepper",
        "Saute onions and garlic until fragrant",
        "Add chicken and brown on all sides",
        "Add tomatoes and rice with broth",
        "Simmer until rice is cooked"
      ],
      "cookingTime": "45 minutes",
      "difficulty": "Medium",
      "nutrition": {
        "calories": 420,
        "protein": "35g",
        "carbs": "45g"
      }
    }
  ],
  "status": "success"
}
```

#### Health Check
```bash
GET /api/health

curl http://localhost:8000/health
```

#### Example Response
```bash
GET /api/example

curl http://localhost:8000/api/example
```

## Project Structure

```
smart-recipe-analyzer/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration management
│   ├── dspy_modules/          # DSPy components
│   │   ├── recipe_analyzer.py # Main recipe generation logic
│   │   └── signatures.py      # DSPy signatures
│   ├── models/                # Pydantic models
│   │   └── schemas.py         # Request/Response schemas
│   └── tools/                 # Utility modules
├── frontend/                  # Frontend application (TBD)
├── tests/                     # Test suite (TBD)
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── run_backend.py            # Server runner script
└── README.md                 # This file
```

## DSPy Architecture

The application leverages DSPy's powerful features:

1. **Signatures**: Define clear input/output specifications
2. **Modules**: Use `ChainOfThought` for complex reasoning
3. **Optimization**: Automatic prompt tuning without manual engineering
4. **Caching**: Efficient repeated requests

### Key DSPy Components

- **RecipeGenerationSignature**: Defines the contract for recipe generation
- **SimpleRecipeGenerator**: Optimized single-call generator for fast responses
- **RecipeAnalyzer**: Full pipeline with validation and enhancement

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `LLM_PROVIDER` | LLM provider (openai/anthropic) | `openai` |
| `LLM_MODEL` | Model name | `gpt-3.5-turbo` |
| `LLM_API_KEY` | API key for LLM | Required |
| `LLM_TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `LLM_MAX_TOKENS` | Max response length | `2000` |
| `DSPY_CACHE_DIR` | Cache directory | `.dspy_cache` |

## Development

### Running in Debug Mode
```bash
export DEBUG=True
python run_backend.py
```

### Testing the API
```python
import requests

# Test with ingredients
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"ingredients": "pasta, garlic, olive oil, parmesan"}
)
print(response.json())
```

### Performance Optimization

The backend uses `SimpleRecipeGenerator` by default for faster responses:
- Single LLM call instead of multiple
- Efficient JSON parsing
- Quick fallback responses
- DSPy caching for repeated requests

## TODO

- [ ] Frontend implementation (React/Vue)
- [ ] User authentication
- [ ] Recipe saving/history
- [ ] Image generation integration
- [ ] Recipe rating system
- [ ] Ingredient substitution suggestions
- [ ] Deployment configuration
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [DSPy](https://github.com/stanfordnlp/dspy) - Stanford's framework for programming LMs
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework for building APIs
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type annotations

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainers.

---

Built with DSPy and FastAPI