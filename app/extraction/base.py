from typing import Protocol
from .schemas import ExtractedItem


class Extractor(Protocol):
    def extract(self, text: str) -> list[ExtractedItem]:
        ...

