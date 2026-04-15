"""baseline

Revision ID: c808e912b067
Revises:
Create Date: 2026-04-02 10:21:14.438631

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op

revision: str = "c808e912b067"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_SYSTEM_PROMPT = (
    "You are an HR assistant for Acme Corp. You help employees and managers "
    "with questions about staff, compensation, team structure, and general HR queries. "
    "Use the employee data provided in context to give accurate, specific answers. "
    "If asked about an employee, reference the data rather than making assumptions."
)


def upgrade() -> None:
    op.create_table(
        "app_settings",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("default_model", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("reasoning_enabled", sa.Boolean(), nullable=False),
        sa.Column("max_context_tokens", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "conversations",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "messages",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("conversation_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("thinking_content", sa.Text(), nullable=True),
        sa.Column("model", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("response_ms", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_messages_conversation_id", "messages", ["conversation_id"])
    op.create_index("idx_messages_created_at", "messages", ["created_at"])

    op.execute(
        sa.text(
            "INSERT INTO app_settings (id, system_prompt, default_model, reasoning_enabled, "
            "max_context_tokens, updated_at) VALUES (:id, :prompt, :model, :reasoning, "
            ":tokens, NOW()) ON CONFLICT (id) DO NOTHING"
        ).bindparams(
            id="default",
            prompt=DEFAULT_SYSTEM_PROMPT,
            model="anthropic/claude-4.6-opus",
            reasoning=True,
            tokens=100000,
        )
    )


def downgrade() -> None:
    op.drop_index("idx_messages_created_at", table_name="messages")
    op.drop_index("idx_messages_conversation_id", table_name="messages")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("app_settings")
