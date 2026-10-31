import os 

from .base import Extractor


def get_extractor() -> Extractor:
    if os.getenv("OPENROUTER_API_KEY"):
        from .openrouter import OpenRouterExtractor
        return OpenRouterExtractor()
    from .local_llm import LocalLLMExtractor
    return LocalLLMExtractor()

