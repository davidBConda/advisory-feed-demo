"""create advisories table

Revision ID: 640c334e1114
Revises:
Create Date: 2026-07-29 13:47:29.264842

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "640c334e1114"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "advisories",
        sa.Column("advisory_id", sa.String(), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.String(), nullable=False),
        sa.Column("updated_at", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("advisory_id"),
    )


def downgrade() -> None:
    op.drop_table("advisories")
