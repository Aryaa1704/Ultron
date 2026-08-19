from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str = "base"
    description: str = "Base JARVIS agent"

    @abstractmethod
    async def run(self, task: str) -> str:
        raise NotImplementedError
