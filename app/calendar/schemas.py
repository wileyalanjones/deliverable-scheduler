from pydantic import BaseModel
from datetime import date

class CalendarEvent(BaseModel):
    title: str
    date: date
    description: str | None = None