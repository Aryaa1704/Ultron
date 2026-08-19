from agents.base_agent import BaseAgent


class BrowserAgent(BaseAgent):
    name = "browser"
    description = "Automates browser interactions for retrieval tasks."

    async def run(self, task: str) -> str:
        return f"Browser agent executed workflow: {task}"
