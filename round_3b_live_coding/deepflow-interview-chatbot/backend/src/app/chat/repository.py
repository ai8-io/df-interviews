import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.chat.models import Conversation, Message


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_conversation(self, title: str | None = None) -> Conversation:
        conversation = Conversation(
            id=str(uuid.uuid4()),
            title=title,
            created_at=datetime.now(UTC),
        )
        self._session.add(conversation)
        await self._session.commit()
        await self._session.refresh(conversation)
        return conversation

    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        result = await self._session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()

    async def list_conversations(self) -> list[Conversation]:
        result = await self._session.execute(
            select(Conversation).order_by(Conversation.created_at.desc())  # type: ignore[arg-type]
        )
        return list(result.scalars().all())

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        thinking_content: str | None = None,
        model: str | None = None,
        response_ms: int | None = None,
    ) -> Message:
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            thinking_content=thinking_content,
            model=model,
            response_ms=response_ms,
            created_at=datetime.now(UTC),
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_messages(self, conversation_id: str) -> list[Message]:
        result = await self._session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())  # type: ignore[arg-type]
        )
        return list(result.scalars().all())
