from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import get_current_user
from backend.database import get_session
from backend.models import Conversation, Message, User
from backend.schemas import ChatRequest, ChatResponse, MessageRead, TokenUsageRead
from backend.services.ai_brain import AIBrainError, ClaudeBrain, get_ai_brain

router = APIRouter(tags=["chat"])


def _default_title(message: str) -> str:
    title = message.strip().replace("\n", " ")[:60]
    return title or "New conversation"


async def _get_or_create_conversation(
    payload: ChatRequest,
    current_user: User,
    session: AsyncSession,
) -> Conversation:
    if payload.conversation_id:
        conversation = await session.scalar(
            select(Conversation).where(
                Conversation.id == payload.conversation_id,
                Conversation.user_id == current_user.id,
            )
        )
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    conversation = Conversation(
        user_id=current_user.id,
        title=payload.title or _default_title(payload.message),
    )
    session.add(conversation)
    await session.flush()
    return conversation


async def _conversation_history(
    conversation_id: str,
    session: AsyncSession,
) -> list[Message]:
    result = await session.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return list(result.all())


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    brain: ClaudeBrain = Depends(get_ai_brain),
):
    conversation = await _get_or_create_conversation(payload, current_user, session)
    history = await _conversation_history(conversation.id, session)

    if payload.stream:
        return StreamingResponse(
            _stream_chat_response(brain, history, payload.message, conversation, session),
            media_type="text/plain; charset=utf-8",
        )

    try:
        brain_response = await brain.complete(history, payload.message)
    except AIBrainError as exc:
        await session.rollback()
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    now = datetime.utcnow()
    user_message = Message(conversation_id=conversation.id, role="user", content=payload.message)
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=brain_response.content,
        input_tokens=brain_response.usage.input_tokens,
        output_tokens=brain_response.usage.output_tokens,
        total_tokens=brain_response.usage.total_tokens,
    )
    conversation.updated_at = now
    session.add_all([user_message, assistant_message])
    await session.commit()
    await session.refresh(assistant_message)

    return ChatResponse(
        conversation_id=conversation.id,
        message=MessageRead.model_validate(assistant_message),
        routed_agent="claude-brain",
        model=brain_response.model,
        token_usage=TokenUsageRead(**brain_response.usage.as_dict()),
    )


async def _stream_chat_response(
    brain: ClaudeBrain,
    history: list[Message],
    message: str,
    conversation: Conversation,
    session: AsyncSession,
):
    chunks: list[str] = []
    try:
        async for chunk in brain.stream(history, message):
            chunks.append(chunk)
            yield chunk
    except AIBrainError as exc:
        await session.rollback()
        yield f"\n[ULTRON error: {exc.detail}]"
        return

    assistant_content = "".join(chunks).strip()
    if assistant_content:
        conversation.updated_at = datetime.utcnow()
        session.add_all([
            Message(conversation_id=conversation.id, role="user", content=message),
            Message(conversation_id=conversation.id, role="assistant", content=assistant_content),
        ])
        await session.commit()
