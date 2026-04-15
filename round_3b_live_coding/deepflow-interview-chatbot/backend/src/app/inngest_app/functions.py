import logging

import inngest
from chat_contracts.events import MessageCreatedEventData

from app.inngest_app.client import client

logger = logging.getLogger(__name__)


@client.create_function(  # ty: ignore[invalid-argument-type]
    fn_id="generate-conversation-title",
    trigger=inngest.TriggerEvent(event="chat/message.created"),
)
async def generate_conversation_title(
    ctx: inngest.Context,
    step: inngest.Step,
) -> None:
    event_data = MessageCreatedEventData(**ctx.event.data)  # ty: ignore[invalid-argument-type]
    logger.info(
        "inngest fn triggered conversation_id=%s message_count=%d role=%s",
        event_data.conversation_id,
        event_data.message_count,
        event_data.role,
    )

    if event_data.message_count != 2:
        logger.info("skipping title generation — message_count != 2")
        return

    logger.info("would generate title for conversation %s", event_data.conversation_id)
    # TODO: call LLM to generate a short title from the first exchange
    # TODO: write title back to the conversations table


def get_functions() -> list[inngest.Function]:
    return [generate_conversation_title]
