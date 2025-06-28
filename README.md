# Smart Recipe Analyzer

An AI-powered web application that generates recipe suggestions with nutritional analysis from a list of ingredients. Built with FastAPI, DSPy, and modern web technologies.

## Demo Videos

### 🤖 Agentic Mode Demo

[![Agentic Recipe Generator Demo](https://img.youtube.com/vi/x2uaiB7PVgU/0.jpg)](https://youtu.be/x2uaiB7PVgU)

_Watch the agentic mode in action with tool-enhanced recipe generation, accurate nutrition calculation, and smart ingredient validation._

### 🧠 Standard Mode Demo

[![Standard Recipe Generator Demo](https://img.youtube.com/vi/JqYX7BkJHd8/0.jpg)](https://youtu.be/JqYX7BkJHd8)

_See the standard mode providing fast recipe generation using pure DSPy modules._

## Overview

Smart Recipe Analyzer uses advanced AI (via DSPy framework) to:

- Generate 2-3 recipe suggestions from your available ingredients
- Provide detailed cooking instructions
- Calculate nutritional information
- Support dietary restrictions (bonus feature)
- Offer a clean, responsive web interface

## Features

### Core Features

- **Dual Mode Operation**: Choose between standard DSPy or agentic tool-based generation
- **Model Selection**: Switch between Anthropic Claude and Google Gemini models
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
- **Language Model**: Supports Anthropic Claude and Google Gemini
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend (Planned)

- React/Vue.js or Vanilla JavaScript
- Responsive design
- Real-time loading states

## Installation

### Prerequisites

- Python 3.13+
- API key for your chosen LLM (Anthropic or Gemini)
- uv (recommended) or pip

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Huvinesh-Rajendran-12/axium-tutorial.git
   cd axium-tutorial
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

   Edit `.env` and add your API credentials. See the [Environment Variables](#environment-variables) section below for all configuration options.

4. **Run the server**

   **Standard Mode (Non-Agentic):**

   ```bash
   python run_backend.py
   # Or
   uv run run_backend.py
   ```

   **Agentic Mode (With Tools):**

   ```bash
   python run_backend.py --agentic
   # Or
   uv run run_backend.py --agentic
   ```

   **Model Selection:**

   ```bash
   # Use Anthropic Claude (default)
   uv run run_backend.py --model anthropic

   # Use Google Gemini
   uv run run_backend.py --model gemini

   # Combine options
   uv run run_backend.py --agentic --model gemini
   ```

   **Additional Options:**

   ```bash
   # Custom host and port
   python run_backend.py --host 127.0.0.1 --port 8080

   # Enable debug mode
   python run_backend.py --debug

   # All options combined
   python run_backend.py --agentic --model anthropic --debug --port 8080
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
      "ingredients": [
        "chicken",
        "rice",
        "tomatoes",
        "onions",
        "garlic"
      ],
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
  "status": "success",
  "mode": "agentic"
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
│   │   ├── recipe_analyzer.py # Standard recipe generation logic
│   │   ├── agentic_analyzer.py# Agentic recipe generation with tools
│   │   └── signatures.py      # DSPy signatures
│   ├── models/                # Pydantic models
│   │   └── schemas.py         # Request/Response schemas
│   └── tools/                 # Agentic tools
│       └── nutrition_calculator.py # Nutrition and cooking tools
├── frontend/                  # Frontend application (TBD)
├── tests/                     # Test suite (TBD)
├── .env.example              # Environment template
├── requirements.txt          # Python dependencies
├── run_backend.py            # Server runner script
└── README.md                 # This file
```

## Dual Mode Architecture

The Smart Recipe Analyzer supports two distinct modes of operation:

### 🧠 Standard Mode (default)

Uses pure DSPy modules for fast generation:

- **Direct LLM generation** with optimized prompts
- **Faster response times** with single API calls
- **Efficient JSON parsing** and validation
- **Lightweight processing** without external tools

### 🤖 Agentic Mode (--agentic)

Uses specialized tools for enhanced accuracy:

- **Tool-based nutrition calculation** with comprehensive ingredient database
- **Smart ingredient validation** and automatic cleanup
- **Realistic cooking time estimation** based on ingredient complexity
- **Structured recipe generation** with validated data
- **Multiple fallback layers** for reliability

## DSPy Architecture

The application leverages DSPy's powerful features with both standard and **agentic approaches**:

1. **Signatures**: Define clear input/output specifications
2. **Modules**: Use `ChainOfThought` for complex reasoning
3. **Optimization**: Automatic prompt tuning without manual engineering
4. **Caching**: Efficient repeated requests

### Key DSPy Components

- **RecipeGenerationSignature**: Defines the contract for recipe generation
- **SimpleRecipeGenerator**: Optimized single-call generator for fast responses
- **SimpleAgenticAnalyzer**: Tool-enhanced generator with nutrition calculation
- **RecipeAnalyzer**: Full pipeline with validation and enhancement

## Configuration

### Environment Variables

All environment variables found in `backend/config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `AGENTIC_MODE` | Enable agentic mode | `False` |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) | `*` |
| `LLM_PROVIDER` | LLM provider (anthropic/gemini) | `anthropic` |
| `LLM_MODEL_ANTHROPIC` | Anthropic model | `anthropic/claude-sonnet-4-20250514` |
| `LLM_MODEL_GEMINI` | Gemini model | `gemini/gemini-2.5-flash` |
| `ANTHROPIC_API_KEY` | Anthropic API key | Required for Anthropic |
| `GEMINI_API_KEY` | Gemini API key | Required for Gemini |
| `LLM_MAX_TOKENS` | Max response length | `2000` |
| `DSPY_CACHE_DIR` | Cache directory | `.dspy_cache` |
| `RATE_LIMIT_REQUESTS` | Rate limit requests per period | `100` |
| `RATE_LIMIT_PERIOD` | Rate limit period in seconds | `3600` |

## Development

### Running in Debug Mode

```bash
python run_backend.py --debug
# Or with other options
uv run run_backend.py --debug --agentic --model gemini
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

**Agentic Mode:**

- Tool-based nutrition calculation (no guessing)
- Smart ingredient validation and cleaning
- Realistic cooking time estimation
- Structured recipe generation with DSPy modules
- Multiple fallback layers for reliability

**Standard Mode:**

- Faster response times with direct LLM calls
- Lightweight processing without external tools
- Efficient JSON parsing and validation
- DSPy caching for repeated requests

### Command Line Usage

```bash
# Show all available options
python run_backend.py --help

# Standard mode with Anthropic
uv run run_backend.py

# Agentic mode with Gemini
uv run run_backend.py --agentic --model gemini

# Debug mode with custom port
uv run run_backend.py --debug --port 8080
```

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
