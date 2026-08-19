class TaskPlanner:
    def plan(self, user_message: str) -> dict[str, str]:
        lower = user_message.lower()
        if "email" in lower:
            return {"agent": "email", "reason": "Detected email intent"}
        if "calendar" in lower or "schedule" in lower:
            return {"agent": "calendar", "reason": "Detected scheduling intent"}
        if "research" in lower or "find" in lower:
            return {"agent": "research", "reason": "Detected research intent"}
        if "browser" in lower or "open" in lower:
            return {"agent": "browser", "reason": "Detected browser intent"}
        return {"agent": "job", "reason": "Default execution path"}
