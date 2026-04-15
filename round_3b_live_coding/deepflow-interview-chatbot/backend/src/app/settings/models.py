from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Text
from sqlmodel import Field, SQLModel


class AppSettings(SQLModel, table=True):
    __tablename__ = "app_settings"

    id: str = Field(default="default", primary_key=True)
    system_prompt: str = Field(sa_column=Column(Text, nullable=False))
    default_model: str = Field(default="anthropic/claude-4.6-opus")
    reasoning_enabled: bool = Field(default=True)
    max_context_tokens: int = Field(default=100000)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
