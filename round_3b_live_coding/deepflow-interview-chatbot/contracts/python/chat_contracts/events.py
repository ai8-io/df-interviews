from pydantic import BaseModel, Field


class MessageCreatedEventData(BaseModel):
    """Payload for the chat/message.created Inngest event."""

    conversation_id: str
    message_id: str
    role: str = Field(
        ..., description="The role of the message author: 'user' or 'assistant'."
    )
    message_count: int = Field(
        ..., description="Total number of messages in the conversation after this one."
    )


class MessageCreatedEvent(BaseModel):
    """Typed envelope for the chat/message.created Inngest event."""

    name: str = Field(default="chat/message.created", frozen=True)
    data: MessageCreatedEventData
