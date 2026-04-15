import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.settings.models import AppSettings
from app.settings.schemas import AppSettingsResponse, AppSettingsUpdate

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are an HR assistant for Acme Corp. You help employees and managers "
    "with questions about staff, compensation, team structure, and general HR queries. "
    "Use the employee data provided in context to give accurate, specific answers. "
    "If asked about an employee, reference the data rather than making assumptions."
)


class SettingsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_settings(self) -> AppSettingsResponse:
        result = await self._session.execute(
            select(AppSettings).where(AppSettings.id == "default")
        )
        settings = result.scalar_one_or_none()

        if not settings:
            settings = AppSettings(
                id="default",
                system_prompt=DEFAULT_SYSTEM_PROMPT,
                default_model="anthropic/claude-4.6-opus",
                reasoning_enabled=True,
                max_context_tokens=100000,
                updated_at=datetime.now(UTC),
            )
            self._session.add(settings)
            await self._session.commit()
            await self._session.refresh(settings)
            logger.info("created default app_settings row")

        return AppSettingsResponse(
            system_prompt=settings.system_prompt,
            default_model=settings.default_model,
            reasoning_enabled=settings.reasoning_enabled,
            max_context_tokens=settings.max_context_tokens,
            updated_at=settings.updated_at.isoformat() if settings.updated_at else None,
        )

    async def update_settings(self, update: AppSettingsUpdate) -> AppSettingsResponse:
        result = await self._session.execute(
            select(AppSettings).where(AppSettings.id == "default")
        )
        settings = result.scalar_one_or_none()

        if not settings:
            await self.get_settings()
            result = await self._session.execute(
                select(AppSettings).where(AppSettings.id == "default")
            )
            settings = result.scalar_one_or_none()

        assert settings is not None

        update_data = update.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(settings, field, value)
        settings.updated_at = datetime.now(UTC)

        await self._session.commit()
        await self._session.refresh(settings)

        logger.info("app_settings updated fields=%s", list(update_data.keys()))

        return AppSettingsResponse(
            system_prompt=settings.system_prompt,
            default_model=settings.default_model,
            reasoning_enabled=settings.reasoning_enabled,
            max_context_tokens=settings.max_context_tokens,
            updated_at=settings.updated_at.isoformat() if settings.updated_at else None,
        )
