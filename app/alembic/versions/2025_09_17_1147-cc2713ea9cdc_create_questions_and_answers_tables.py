"""Create questions and answers tables

Revision ID: cc2713ea9cdc
Revises: bcd354de27f2
Create Date: 2025-09-17 11:47:48.272816

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "cc2713ea9cdc"
down_revision: Union[str, Sequence[str], None] = "bcd354de27f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "questions",
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_questions")),
        sa.UniqueConstraint("text", name=op.f("uq_questions_text")),
    )
    op.create_table(
        "answers",
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name=op.f("fk_answers_question_id_questions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_answers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("answers")
    op.drop_table("questions")
