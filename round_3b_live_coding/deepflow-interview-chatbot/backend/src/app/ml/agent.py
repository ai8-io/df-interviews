import logging
from functools import lru_cache

from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel, OpenRouterModelSettings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an HR assistant for Acme Corp. You help employees and managers "
    "with questions about staff, compensation, team structure, and general HR queries. "
    "Use the employee data provided in context to give accurate, specific answers. "
    "If asked about an employee, reference the data rather than making assumptions."
)

MODEL_SETTINGS = OpenRouterModelSettings(
    openrouter_reasoning={"effort": "high"},
    temperature=0.3,
)


@lru_cache
def get_agent(model_name: str = "anthropic/claude-4.6-opus") -> Agent[None, str]:
    logger.info("initialising agent model=%s", model_name)
    model = OpenRouterModel(model_name)
    return Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        model_settings=MODEL_SETTINGS,
    )
