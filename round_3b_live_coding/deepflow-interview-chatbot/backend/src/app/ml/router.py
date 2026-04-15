import logging

from chat_contracts import SendMessageRequest, SendMessageResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.ml.service import MLService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


@router.post("/api/chat", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str | None]:
    logger.info(
        "POST /api/chat conversation_id=%s model=%s msg_len=%d",
        request.conversation_id,
        request.model,
        len(request.message),
    )
    service = MLService(session)
    return await service.run_chat(
        message=request.message,
        conversation_id=request.conversation_id,
        model=request.model,
    )
