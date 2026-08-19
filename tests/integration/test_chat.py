import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from backend.auth import get_current_user
from backend.database import get_session
from backend.main import app
from sqlalchemy import select

from backend.models import Base, Message, User
from backend.services.ai_brain import AIBrainError, BrainResponse, TokenUsage, get_ai_brain


class FakeBrain:
    model = "claude-test"
    context_window = 2

    def __init__(self):
        self.seen_history = None

    def build_messages(self, history, latest_user_message):
        recent = list(history)[-self.context_window :]
        return [
            {"role": item.role, "content": item.content}
            for item in recent
        ] + [{"role": "user", "content": latest_user_message}]

    async def complete(self, history, latest_user_message):
        self.seen_history = self.build_messages(history, latest_user_message)
        return BrainResponse(
            content=f"Claude says: {latest_user_message}",
            model=self.model,
            usage=TokenUsage(input_tokens=10, output_tokens=5),
        )


class FailingBrain(FakeBrain):
    async def complete(self, history, latest_user_message):
        raise AIBrainError()


@pytest.fixture
async def chat_client():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    user = User(email="builder@example.com", hashed_password="not-used", full_name="Builder")
    async with session_factory() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)

    async def override_session():
        async with session_factory() as session:
            yield session

    async def override_user():
        return user

    fake_brain = FakeBrain()
    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_current_user] = override_user
    app.dependency_overrides[get_ai_brain] = lambda: fake_brain

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client, fake_brain, session_factory

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.asyncio
async def test_chat_persists_claude_response_with_usage(chat_client):
    client, fake_brain, session_factory = chat_client

    response = await client.post("/chat", json={"message": "Help me plan today"})

    assert response.status_code == 200
    body = response.json()
    assert body["message"]["content"] == "Claude says: Help me plan today"
    assert body["routed_agent"] == "claude-brain"
    assert body["model"] == "claude-test"
    assert body["token_usage"] == {
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
    }

    async with session_factory() as session:
        messages = (await session.scalars(select(Message))).all()
    assert len(messages) == 2


@pytest.mark.asyncio
async def test_chat_uses_bounded_recent_history(chat_client):
    client, fake_brain, _ = chat_client

    first = await client.post("/chat", json={"message": "one"})
    conversation_id = first.json()["conversation_id"]
    await client.post("/chat", json={"conversation_id": conversation_id, "message": "two"})

    assert fake_brain.seen_history == [
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "Claude says: one"},
        {"role": "user", "content": "two"},
    ]


@pytest.mark.asyncio
async def test_chat_provider_failure_returns_controlled_error(chat_client):
    client, _, _ = chat_client
    app.dependency_overrides[get_ai_brain] = lambda: FailingBrain()

    response = await client.post("/chat", json={"message": "fail safely"})

    assert response.status_code == 502
    assert response.json() == {"detail": "AI brain is temporarily unavailable"}


@pytest.mark.asyncio
async def test_chat_still_rejects_unauthenticated_users():
    app.dependency_overrides.clear()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat", json={"message": "hello"})
    assert response.status_code == 403
