from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_conversations: int
    total_messages: int
    avg_messages_per_conversation: float
    total_user_messages: int
    total_assistant_messages: int


class ResponseTimeStats(BaseModel):
    avg_response_ms: float
    p50_response_ms: float
    p95_response_ms: float
    slowest_response_ms: float
    total_measured: int


class ModelUsageEntry(BaseModel):
    model: str
    message_count: int
    avg_response_ms: float | None


class ModelUsageStats(BaseModel):
    entries: list[ModelUsageEntry]
    total_messages_with_model: int


class DailyMessageCount(BaseModel):
    date: str
    count: int


class ConversationActivity(BaseModel):
    daily_messages: list[DailyMessageCount]
    busiest_day: str | None
    total_days_active: int
