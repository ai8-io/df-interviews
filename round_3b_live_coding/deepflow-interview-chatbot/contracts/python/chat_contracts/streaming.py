from enum import StrEnum

from pydantic import BaseModel, Field


class ChunkType(StrEnum):
    CONTENT = "content"
    THINKING = "thinking"
    DONE = "done"
    ERROR = "error"


class ThinkingMetadata(BaseModel):
    """Metadata attached to thinking/reasoning chunks from the model."""

    content: str = Field(default="", description="The thinking text so far.")
    is_complete: bool = Field(
        default=False,
        description="Whether this thinking block has finished streaming.",
    )


class ChatChunk(BaseModel):
    """A single streaming chunk sent over SSE.

    Used as the envelope for all streaming events. The `thinking` field
    carries reasoning metadata when the model is configured with
    reasoning enabled — the frontend currently ignores this field.
    """

    type: ChunkType
    content: str = ""
    thinking: ThinkingMetadata | None = Field(
        default=None,
        description="Thinking metadata when this chunk is part of a reasoning turn.",
    )
    conversation_id: str | None = None
    message_id: str | None = None
