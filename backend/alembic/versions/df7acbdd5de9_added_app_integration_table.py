"""Added app integration table

Revision ID: df7acbdd5de9
Revises: 3b29fb67f3ff
Create Date: 2025-03-24 15:59:07.564189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df7acbdd5de9'
down_revision: Union[str, None] = '3b29fb67f3ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'app_integrations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('app_name', sa.String(length=150), nullable=False),
        sa.Column('token', sa.String(length=500), nullable=False),
        sa.Column('refresh_token', sa.String(length=500), nullable=True),
        sa.Column('expire', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('app_integrations')
