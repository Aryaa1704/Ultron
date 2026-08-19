from agents.base_agent import BaseAgent


class CalendarAgent(BaseAgent):
    name = "calendar"
    description = "Schedules events and resolves availability."

    async def run(self, task: str) -> str:
        return f"Calendar agent processed task: {task}"
