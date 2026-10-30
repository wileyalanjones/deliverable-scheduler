import os

from dotenv import load_dotenv

from .base import Extractor
from .local_llm import LocalLLMExtractor
from .openrouter import OpenRouterExtractor

load_dotenv()


def get_extractor() -> Extractor:
    """Return the best available extractor.

    Uses OpenRouter when ``OPENROUTER_API_KEY`` is set (better accuracy),
    otherwise falls back to the bundled local model (no key required).
    """
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenRouterExtractor()
    return LocalLLMExtractor()