from agents.base_agent import BaseAgent


class JobAgent(BaseAgent):
    name = "job"
    description = "Tracks long-running and queued tasks."

    async def run(self, task: str) -> str:
        return f"Job agent registered task: {task}"
