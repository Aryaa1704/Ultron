from agents.base_agent import BaseAgent


class EmailAgent(BaseAgent):
    name = "email"
    description = "Handles inbox triage and outgoing email drafting."

    async def run(self, task: str) -> str:
        return f"Email agent queued task: {task}"
