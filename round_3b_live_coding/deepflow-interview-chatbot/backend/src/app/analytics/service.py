import logging
from collections import defaultdict
from datetime import datetime

from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.analytics.schemas import (
    AnalyticsOverview,
    ConversationActivity,
    DailyMessageCount,
    ModelUsageEntry,
    ModelUsageStats,
    ResponseTimeStats,
)
from app.chat.models import Conversation, Message

logger = logging.getLogger(__name__)


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_overview(self) -> AnalyticsOverview:
        conv_count = await self._session.execute(
            select(func.count()).select_from(Conversation)
        )
        total_convos: int = conv_count.scalar() or 0

        msg_count = await self._session.execute(
            select(func.count()).select_from(Message)
        )
        total_msgs: int = msg_count.scalar() or 0

        user_count = await self._session.execute(
            select(func.count()).select_from(Message).where(Message.role == "user")
        )
        total_user: int = user_count.scalar() or 0

        assistant_count = await self._session.execute(
            select(func.count()).select_from(Message).where(Message.role == "assistant")
        )
        total_assistant: int = assistant_count.scalar() or 0

        avg_msgs = total_msgs / total_convos if total_convos > 0 else 0.0

        logger.info(
            "analytics overview conversations=%d messages=%d avg=%.1f",
            total_convos,
            total_msgs,
            avg_msgs,
        )

        return AnalyticsOverview(
            total_conversations=total_convos,
            total_messages=total_msgs,
            avg_messages_per_conversation=round(avg_msgs, 1),
            total_user_messages=total_user,
            total_assistant_messages=total_assistant,
        )

    async def get_response_times(self) -> ResponseTimeStats:
        result = await self._session.execute(
            select(Message.response_ms)
            .where(Message.response_ms.is_not(None))  # type: ignore[union-attr]
            .where(Message.role == "assistant")
            .order_by(Message.response_ms.asc())  # type: ignore[union-attr]
        )
        times: list[int] = [row[0] for row in result.fetchall()]

        if not times:
            return ResponseTimeStats(
                avg_response_ms=0,
                p50_response_ms=0,
                p95_response_ms=0,
                slowest_response_ms=0,
                total_measured=0,
            )

        n = len(times)
        p50_idx = n // 2
        p95_idx = min(int(n * 0.95), n - 1)

        return ResponseTimeStats(
            avg_response_ms=round(sum(times) / n, 1),
            p50_response_ms=float(times[p50_idx]),
            p95_response_ms=float(times[p95_idx]),
            slowest_response_ms=float(times[-1]),
            total_measured=n,
        )

    async def get_model_usage(self) -> ModelUsageStats:
        result = await self._session.execute(
            select(
                Message.model,
                func.count().label("count"),
                func.avg(Message.response_ms).label("avg_ms"),
            )
            .where(Message.model.is_not(None))  # type: ignore[union-attr]
            .where(Message.role == "assistant")
            .group_by(Message.model)
            .order_by(text("count DESC"))
        )
        rows = result.fetchall()

        entries = [
            ModelUsageEntry(
                model=row[0] or "unknown",
                message_count=row[1],
                avg_response_ms=round(row[2], 1) if row[2] else None,
            )
            for row in rows
        ]
        total = sum(e.message_count for e in entries)

        return ModelUsageStats(entries=entries, total_messages_with_model=total)

    async def get_activity(self) -> ConversationActivity:
        result = await self._session.execute(
            select(Message.created_at).order_by(Message.created_at.asc())  # type: ignore[arg-type]
        )
        timestamps = [row[0] for row in result.fetchall()]

        daily: dict[str, int] = defaultdict(int)
        for ts in timestamps:
            if isinstance(ts, datetime):
                day = ts.strftime("%Y-%m-%d")
                daily[day] += 1

        daily_messages = [
            DailyMessageCount(date=date, count=count)
            for date, count in sorted(daily.items())
        ]

        busiest = max(daily.items(), key=lambda x: x[1])[0] if daily else None

        return ConversationActivity(
            daily_messages=daily_messages,
            busiest_day=busiest,
            total_days_active=len(daily),
        )
