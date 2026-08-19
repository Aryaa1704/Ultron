from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ErrorResponse(BaseModel):
    detail: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageRead(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationRead(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ConversationListResponse(BaseModel):
    conversations: list[ConversationRead]


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1)
    memory_type: str = Field(default="short_term", min_length=1, max_length=50)
    metadata_json: dict = Field(default_factory=dict)


class MemoryRead(BaseModel):
    id: str
    user_id: str
    content: str
    memory_type: str
    metadata_json: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    is_active: bool = True


class AgentRead(BaseModel):
    id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    agent_id: str | None = None
    payload: dict = Field(default_factory=dict)
    status: str = Field(default="pending", min_length=1, max_length=50)


class TaskRead(BaseModel):
    id: str
    user_id: str
    agent_id: str | None
    status: str
    payload: dict
    result: dict | None
    error_message: str | None
    retries: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentRunRequest(BaseModel):
    agent_name: str = Field(min_length=1)
    task: str = Field(min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None
    title: str | None = Field(default=None, max_length=255)


class ChatResponse(BaseModel):
    conversation_id: str
    message: MessageRead
    routed_agent: str | None = None
