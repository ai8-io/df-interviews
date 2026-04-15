from pydantic import BaseModel, Field


class AppSettingsResponse(BaseModel):
    system_prompt: str
    default_model: str
    reasoning_enabled: bool
    max_context_tokens: int
    updated_at: str | None = None


class AppSettingsUpdate(BaseModel):
    system_prompt: str | None = Field(None, min_length=10)
    default_model: str | None = None
    reasoning_enabled: bool | None = None
    max_context_tokens: int | None = Field(None, ge=1000, le=500000)
