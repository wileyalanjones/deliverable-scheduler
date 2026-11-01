from .schemas import CalendarEvent


class MockCalendarProvider:
    def __init__(self):
        self.events: dict[str, CalendarEvent] = {}
        self._counter = 0

    def create_event(self, event: CalendarEvent) -> str:
        self._counter += 1
        event_id = f"mock-{self._counter}"
        self.events[event_id] = event                
        return event_id

    def list_events(self) -> dict[str, CalendarEvent]:
        return self.events

    def delete_event(self, event_id: str) -> None:
        self.events.pop(event_id, None)              

    def clear(self) -> None:
        self.events.clear()
        self._counter = 0