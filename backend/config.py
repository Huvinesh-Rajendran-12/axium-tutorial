import os
from pathlib import Path

import dspy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_VERSION = "1.0.0"
API_TITLE = "Smart Recipe Analyzer API"
API_DESCRIPTION = "Generate recipes with nutritional analysis from ingredients using AI"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, anthropic, etc.
LLM_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-20250514")
LLM_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2000"))

# DSPy Configuration
DSPY_CACHE_DIR = Path(os.getenv("DSPY_CACHE_DIR", ".dspy_cache"))
DSPY_CACHE_DIR.mkdir(exist_ok=True)

# Rate Limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))  # seconds


# Initialize DSPy
def init_dspy():
    """Initialize DSPy with configured LLM."""
    if not LLM_API_KEY:
        raise ValueError("LLM_API_KEY environment variable is not set")

        # Default to OpenAI-compatible endpoint
    lm = dspy.LM(
        model="gemini/gemini-2.5-flash",
        api_key="AIzaSyDXX25eYmZU4XMGCvzeWK5DJr1Of-Q9C3U",
        max_tokens=LLM_MAX_TOKENS,
    )

    # Configure DSPy
    dspy.settings.configure(lm=lm, cache_dir=str(DSPY_CACHE_DIR))

    return lm
