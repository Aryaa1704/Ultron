from orchestrator.planner import TaskPlanner


def test_planner_routes_email() -> None:
    planner = TaskPlanner()
    decision = planner.plan("Draft an email to the operations team")
    assert decision["agent"] == "email"


def test_planner_routes_schedule() -> None:
    planner = TaskPlanner()
    decision = planner.plan("Schedule a design sync for tomorrow")
    assert decision["agent"] == "calendar"
