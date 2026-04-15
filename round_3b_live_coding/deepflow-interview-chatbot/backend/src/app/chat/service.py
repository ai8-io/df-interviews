import logging

import inngest
from chat_contracts.events import MessageCreatedEventData
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models import Conversation, Message
from app.chat.repository import ChatRepository
from app.inngest_app.client import client as inngest_client

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ChatRepository(session)

    async def get_or_create_conversation(
        self,
        conversation_id: str | None = None,
    ) -> Conversation:
        if conversation_id:
            existing = await self._repo.get_conversation(conversation_id)
            if existing:
                return existing
        return await self._repo.create_conversation()

    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        thinking_content: str | None = None,
        model: str | None = None,
        response_ms: int | None = None,
    ) -> Message:
        message = await self._repo.add_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            thinking_content=thinking_content,
            model=model,
            response_ms=response_ms,
        )
        logger.info(
            "message saved conversation_id=%s role=%s message_id=%s model=%s response_ms=%s",
            conversation_id,
            role,
            message.id,
            model,
            response_ms,
        )

        messages = await self._repo.get_messages(conversation_id)
        try:
            event_data = MessageCreatedEventData(
                conversation_id=conversation_id,
                message_id=message.id,
                role=role,
                message_count=len(messages),
            )
            await inngest_client.send(
                inngest.Event(
                    name="chat/message.created",
                    data=event_data.model_dump(),
                )
            )
            logger.info(
                "inngest event emitted chat/message.created message_count=%d",
                len(messages),
            )
        except Exception:
            logger.warning("inngest event emission failed", exc_info=True)

        return message

    async def get_messages(self, conversation_id: str) -> list[Message]:
        return await self._repo.get_messages(conversation_id)

    async def list_conversations(self) -> list[Conversation]:
        return await self._repo.list_conversations()
