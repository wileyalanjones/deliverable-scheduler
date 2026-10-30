from datetime import date
from pydantic import BaseModel, Field


class ExtractedItem(BaseModel):
    title: str
    deliverable_date: date
    confidence: float = Field(ge=0.0, le=1.0)
    description: str | None = None
    source_quote: str | None = None

    
