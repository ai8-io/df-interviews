import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.service import ChatService
from app.database import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("")
async def list_conversations(
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    logger.info("GET /api/conversations")
    service = ChatService(session)
    conversations = await service.list_conversations()
    return [
        {
            "id": c.id,
            "title": c.title,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in conversations
    ]


@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    logger.info("GET /api/conversations/%s/messages", conversation_id)
    service = ChatService(session)
    messages = await service.get_messages(conversation_id)
    return [
        {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "role": m.role,
            "content": m.content,
            "thinking_content": m.thinking_content,
            "model": m.model,
            "response_ms": m.response_ms,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in messages
    ]
