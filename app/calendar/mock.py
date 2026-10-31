from .schemas import CalendarEvent

class MockCalendarProvider:
    def __init__(self):
        self.events: list[CalendarEvent] = []
        self._counter = 0

    def create_event(self, event: CalendarEvent) -> str:
        self._counter += 1
        self.events.append(event)
        return f"mock-{self._counter}"

    def list_events(self):
        return self.events 

    