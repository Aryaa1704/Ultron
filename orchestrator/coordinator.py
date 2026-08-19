from orchestrator.planner import TaskPlanner


class AgentCoordinator:
    def __init__(self) -> None:
        self.planner = TaskPlanner()

    def route_task(self, user_message: str) -> str:
        decision = self.planner.plan(user_message)
        return decision["agent"]
