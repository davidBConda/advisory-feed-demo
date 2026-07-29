"""create feed_runs table

Revision ID: 6f609202efd0
Revises: 640c334e1114
Create Date: 2026-07-29 13:52:39.588937

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "6f609202efd0"
down_revision: Union[str, Sequence[str], None] = "640c334e1114"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feed_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.Column("watermark", sa.String(), nullable=False),
        sa.Column("fetch_duration_sec", sa.Float(), nullable=False),
        sa.Column("page_count", sa.Integer(), nullable=False),
        sa.Column("page_timings", sa.JSON(), nullable=False),
        sa.Column("advisories_fetched", sa.Integer(), nullable=False),
        sa.Column("inserted", sa.Integer(), nullable=False),
        sa.Column("updated", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("feed_runs")
