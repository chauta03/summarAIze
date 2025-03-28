"""Add users and meetings table

Revision ID: 3b29fb67f3ff
Revises: 
Create Date: 2025-03-17 17:32:10.497355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3b29fb67f3ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(length=150), nullable=False),
        sa.Column('last_name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=250), unique=True, nullable=False),
        sa.Column('password', sa.String(length=250), nullable=False)
    )

    # Create meetings table
    op.create_table(
        'meetings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('meeting_id', sa.String(length=150), nullable=True),
        sa.Column('meeting_url', sa.String(length=250), nullable=False),
        sa.Column('transcription', sa.String(length=500), nullable=True),
        sa.Column('summary', sa.String(length=500), nullable=True),
        sa.Column('duration', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=True)
    )

def downgrade() -> None:
    """Downgrade schema."""
    # Drop meetings table
    op.drop_table('meetings')

    # Drop users table
    op.drop_table('users')
