import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.schemas import (
    AnalyticsOverview,
    ConversationActivity,
    ModelUsageStats,
    ResponseTimeStats,
)
from app.analytics.service import AnalyticsService
from app.database import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
async def get_overview(
    session: AsyncSession = Depends(get_session),
) -> AnalyticsOverview:
    logger.info("GET /api/analytics/overview")
    service = AnalyticsService(session)
    return await service.get_overview()


@router.get("/response-times", response_model=ResponseTimeStats)
async def get_response_times(
    session: AsyncSession = Depends(get_session),
) -> ResponseTimeStats:
    logger.info("GET /api/analytics/response-times")
    service = AnalyticsService(session)
    return await service.get_response_times()


@router.get("/model-usage", response_model=ModelUsageStats)
async def get_model_usage(
    session: AsyncSession = Depends(get_session),
) -> ModelUsageStats:
    logger.info("GET /api/analytics/model-usage")
    service = AnalyticsService(session)
    return await service.get_model_usage()


@router.get("/activity", response_model=ConversationActivity)
async def get_activity(
    session: AsyncSession = Depends(get_session),
) -> ConversationActivity:
    logger.info("GET /api/analytics/activity")
    service = AnalyticsService(session)
    return await service.get_activity()
