from fastapi import APIRouter, Depends, HTTPException

from agents.browser_agent import BrowserAgent
from agents.calendar_agent import CalendarAgent
from agents.email_agent import EmailAgent
from agents.job_agent import JobAgent
from agents.research_agent import ResearchAgent
from backend.auth import get_current_user
from backend.models import User
from backend.schemas import AgentRunRequest

router = APIRouter(prefix="/agents", tags=["agents"])

AGENT_REGISTRY = {
    "email": EmailAgent(),
    "calendar": CalendarAgent(),
    "research": ResearchAgent(),
    "browser": BrowserAgent(),
    "job": JobAgent(),
}


@router.get("/")
async def list_agents(current_user: User = Depends(get_current_user)) -> dict[str, list[str]]:
    _ = current_user
    return {"agents": list(AGENT_REGISTRY.keys())}


@router.post("/run")
async def run_agent(
    payload: AgentRunRequest,
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    _ = current_user
    agent = AGENT_REGISTRY.get(payload.agent_name.lower())
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    result = await agent.run(payload.task)
    return {"agent": payload.agent_name, "result": result}
