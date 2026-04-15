from pydantic import BaseModel, Field

AVAILABLE_MODELS = [
    "anthropic/claude-4.6-opus",
    "openai/gpt-5.4",
    "google/gemini-3.1",
]

DEFAULT_MODEL = "anthropic/claude-4.6-opus"


class SendMessageRequest(BaseModel):
    """Request body for POST /api/chat."""

    message: str = Field(..., min_length=1)
    conversation_id: str | None = Field(
        default=None,
        description="Existing conversation to continue. If None, a new conversation is created.",
    )
    model: str = Field(
        default=DEFAULT_MODEL,
        description="OpenRouter model identifier to use for this request.",
    )
    reasoning: bool = Field(
        default=True,
        description="Whether to enable model reasoning/thinking for higher quality responses.",
    )


class SendMessageResponse(BaseModel):
    """Response body for POST /api/chat (non-streaming)."""

    conversation_id: str
    message_id: str
    content: str
    thinking_content: str | None = Field(
        default=None,
        description="Raw reasoning content from the model, if reasoning was enabled.",
    )
