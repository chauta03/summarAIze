"""Update meetings table

Revision ID: b08849f84f0d
Revises: df7acbdd5de9
Create Date: 2025-03-28 09:14:06.479385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b08849f84f0d'
down_revision: Union[str, None] = 'df7acbdd5de9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Alter meeting_id and meeting_url to be nullable
    with op.batch_alter_table('meetings') as batch_op:
        batch_op.alter_column('meeting_id', nullable=True)
        batch_op.alter_column('meeting_url', nullable=True)

    # Add record_url column
    op.add_column('meetings', sa.Column('record_url', sa.String(length=250), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove record_url column
    op.drop_column('meetings', 'record_url')

    # Revert meeting_id and meeting_url to be non-nullable
    with op.batch_alter_table('meetings') as batch_op:
        batch_op.alter_column('meeting_id', nullable=False)
        batch_op.alter_column('meeting_url', nullable=False)