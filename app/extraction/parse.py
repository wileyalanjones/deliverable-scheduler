import json
import re

from pydantic import ValidationError

from .schemas import ExtractedItem


def parse_extracted_items(content: str) -> list[ExtractedItem]:
    cleaned = re.sub(r"```[a-zA-Z]*", "", content)
    start, end = cleaned.find("["), cleaned.rfind("]")
    if start == -1 or end == -1 or end < start:
        return []

    try:
        raw = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError:
        return []

    if not isinstance(raw, list):
        return []

    items: list[ExtractedItem] = []
    for obj in raw:
        if not isinstance(obj, dict):
            continue
        try:
            items.append(ExtractedItem.model_validate(obj))
        except ValidationError:
            continue
    return items