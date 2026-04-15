import logging
import time

from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.service import ChatService
from app.clients.service import ClientService
from app.ml.agent import get_agent

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self, session: AsyncSession) -> None:
        self._chat_service = ChatService(session)
        self._client_service = ClientService()

    async def run_chat(
        self,
        message: str,
        conversation_id: str | None = None,
        model: str = "anthropic/claude-4.6-opus",
    ) -> dict[str, str | None]:
        logger.info(
            "run_chat called conversation_id=%s model=%s", conversation_id, model
        )

        conversation = await self._chat_service.get_or_create_conversation(
            conversation_id
        )
        logger.info("conversation resolved id=%s", conversation.id)

        await self._chat_service.save_message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        t0 = time.perf_counter()
        employee_context = self._client_service.format_employee_context()
        ctx_ms = (time.perf_counter() - t0) * 1000
        logger.info(
            "employee context loaded chars=%d time_ms=%.1f",
            len(employee_context),
            ctx_ms,
        )

        augmented_prompt = (
            f"Here is the complete Acme Corp employee database:\n"
            f"---\n{employee_context}\n---\n\n"
            f"User question: {message}"
        )

        agent = get_agent(model)
        t0 = time.perf_counter()
        result = await agent.run(augmented_prompt)
        llm_ms = (time.perf_counter() - t0) * 1000
        response_ms = int(llm_ms)
        logger.info("agent.run completed model=%s time_ms=%.1f", model, llm_ms)

        thinking_content: str | None = None
        for part in result.all_messages():
            if hasattr(part, "parts"):
                for p in part.parts:
                    if hasattr(p, "content") and type(p).__name__ == "ThinkingPart":
                        content: str = str(p.content)
                        thinking_content = (thinking_content or "") + content

        if thinking_content:
            logger.info("thinking content extracted chars=%d", len(thinking_content))

        assistant_msg = await self._chat_service.save_message(
            conversation_id=conversation.id,
            role="assistant",
            content=result.output,
            thinking_content=thinking_content,
            model=model,
            response_ms=response_ms,
        )

        logger.info(
            "chat turn complete conversation_id=%s message_id=%s",
            conversation.id,
            assistant_msg.id,
        )

        return {
            "conversation_id": conversation.id,
            "message_id": assistant_msg.id,
            "content": result.output,
            "thinking_content": thinking_content,
        }
