class CalendarTool:
    async def create_event(self, title: str, start_iso: str, end_iso: str) -> str:
        return f"Prepared calendar event '{title}' from {start_iso} to {end_iso}."
