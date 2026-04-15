import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.settings.schemas import AppSettingsResponse, AppSettingsUpdate
from app.settings.service import SettingsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=AppSettingsResponse)
async def get_settings(
    session: AsyncSession = Depends(get_session),
) -> AppSettingsResponse:
    logger.info("GET /api/settings")
    service = SettingsService(session)
    return await service.get_settings()


@router.put("", response_model=AppSettingsResponse)
async def update_settings(
    update: AppSettingsUpdate,
    session: AsyncSession = Depends(get_session),
) -> AppSettingsResponse:
    logger.info("PUT /api/settings")
    service = SettingsService(session)
    return await service.update_settings(update)
