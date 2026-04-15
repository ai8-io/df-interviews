import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    """A single chat message persisted in the database."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    role: Role
    content: str
    thinking_content: str | None = Field(
        default=None,
        description="Raw reasoning/thinking content produced by the model, if any.",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
