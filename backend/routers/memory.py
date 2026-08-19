from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import get_current_user
from backend.database import get_session
from backend.models import Memory, User
from backend.schemas import MemoryCreate, MemoryRead

router = APIRouter(prefix="/memory", tags=["memory"])


@router.post("/", response_model=MemoryRead, status_code=status.HTTP_201_CREATED)
async def store_memory(
    payload: MemoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> MemoryRead:
    entry = Memory(
        user_id=current_user.id,
        content=payload.content,
        memory_type=payload.memory_type,
        metadata_json=payload.metadata_json,
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return MemoryRead.model_validate(entry)


@router.get("/{memory_id}", response_model=MemoryRead)
async def get_memory(
    memory_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> MemoryRead:
    memory = await session.scalar(
        select(Memory).where(
            Memory.id == memory_id,
            Memory.user_id == current_user.id,
        )
    )
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found")
    return MemoryRead.model_validate(memory)
