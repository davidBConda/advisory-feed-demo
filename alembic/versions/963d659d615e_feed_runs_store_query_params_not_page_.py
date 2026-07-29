"""feed_runs store query params not page stats

Revision ID: 963d659d615e
Revises: 6f609202efd0
Create Date: 2026-07-29 14:00:13.593951

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import sqlite

revision: str = "963d659d615e"
down_revision: Union[str, Sequence[str], None] = "6f609202efd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("feed_runs", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "query_params",
                sa.JSON(),
                nullable=False,
                server_default=sa.text("'{}'"),
            )
        )
        batch_op.drop_column("page_timings")
        batch_op.drop_column("page_count")

    with op.batch_alter_table("feed_runs", schema=None) as batch_op:
        batch_op.alter_column("query_params", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("feed_runs", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "page_count",
                sa.Integer(),
                nullable=False,
                server_default=sa.text("0"),
            )
        )
        batch_op.add_column(
            sa.Column(
                "page_timings",
                sqlite.JSON(),
                nullable=False,
                server_default=sa.text("'[]'"),
            )
        )
        batch_op.drop_column("query_params")

    with op.batch_alter_table("feed_runs", schema=None) as batch_op:
        batch_op.alter_column("page_count", server_default=None)
        batch_op.alter_column("page_timings", server_default=None)
