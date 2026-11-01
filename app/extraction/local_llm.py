import json
import re
from typing import cast
from transformers import pipeline
from pydantic import ValidationError

from .base import Extractor
from .prompt import build_messages
from .schemas import ExtractedItem


_pipeline = None

def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct", device="cpu")
    return _pipeline


def _parse_json_array(raw: str) -> list:
    raw = re.sub(r"```[a-zA-Z]*", "", raw)         
    start, end = raw.find("["), raw.rfind("]")
    if start == -1 or end == -1 or end < start:
        return []
    try:
        return json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return []


class LocalLLMExtractor(Extractor):
    def extract(self, text: str) -> list[ExtractedItem]:
        pipe = _get_pipeline()                    
        messages = build_messages(text)
        result = cast(
            str,
            pipe(
                messages,
                max_new_tokens=2048,
                do_sample=False,
                return_full_text=False,
            )[0]["generated_text"],
        )

        raw_items = _parse_json_array(result)     
        items = []                                
        for obj in raw_items:
            try:
                items.append(ExtractedItem.model_validate(obj))
            except ValidationError:
                continue
        return items
