from typing import Protocol
from .schemas import CalendarEvent

class CalendarProvider(Protocol):
    def create_event(self, event: CalendarEvent) -> str:
        ...

