from agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    name = "research"
    description = "Performs web and document research with source tracking."

    async def run(self, task: str) -> str:
        return f"Research agent started investigation: {task}"
