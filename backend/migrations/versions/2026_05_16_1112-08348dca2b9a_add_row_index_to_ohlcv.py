"""add_row_index_to_ohlcv

Revision ID: 08348dca2b9a
Revises: 05acc664bbb6
Create Date: 2026-05-16 11:12:33.156665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08348dca2b9a'
down_revision: Union[str, None] = '05acc664bbb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema — only add row_index to OhlcvData."""
    with op.batch_alter_table('OhlcvData', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('row_index', sa.Integer(), nullable=False, server_default='0')
        )


def downgrade() -> None:
    """Downgrade schema — remove row_index from OhlcvData."""
    with op.batch_alter_table('OhlcvData', schema=None) as batch_op:
        batch_op.drop_column('row_index')
