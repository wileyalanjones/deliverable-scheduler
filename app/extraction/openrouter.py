import os 
import requests

from .base import Extractor
from .parse import parse_extracted_items
from .prompt import build_messages
from .schemas import ExtractedItem

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-4o-mini"


class OpenRouterExtractor(Extractor):
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
        if not self.api_key:
            raise ValueError(
                "OpenRouterExtractor requires an api key. "
                "Set it in a .env file or you environment."
            )


    def extract(self, text: str) -> list[ExtractedItem]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": build_messages(text),
            "max_tokens": 1000,
        }

        response = requests.post(
            OPENROUTER_URL,
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        return parse_extracted_items(content)