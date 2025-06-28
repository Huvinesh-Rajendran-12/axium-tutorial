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

# Mode Configuration
AGENTIC_MODE = os.getenv("AGENTIC_MODE", "False").lower() == "true"

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # anthropic, gemini
LLM_MODEL_ANTHROPIC = os.getenv(
    "LLM_MODEL_ANTHROPIC", "anthropic/claude-sonnet-4-20250514"
)
LLM_MODEL_GEMINI = os.getenv("LLM_MODEL_GEMINI", "gemini/gemini-2.5-flash")
LLM_API_KEY_ANTHROPIC = os.getenv("ANTHROPIC_API_KEY", "")
LLM_API_KEY_GEMINI = os.getenv("GEMINI_API_KEY", "")
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
    if LLM_PROVIDER == "anthropic":
        if not LLM_API_KEY_ANTHROPIC:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        model = LLM_MODEL_ANTHROPIC
        api_key = LLM_API_KEY_ANTHROPIC
    elif LLM_PROVIDER == "gemini":
        if not LLM_API_KEY_GEMINI:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        model = LLM_MODEL_GEMINI
        api_key = LLM_API_KEY_GEMINI
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

    lm = dspy.LM(
        model=model,
        api_key=api_key,
        max_tokens=LLM_MAX_TOKENS,
    )

    # Configure DSPy
    dspy.settings.configure(lm=lm, cache_dir=str(DSPY_CACHE_DIR))

    return lm
