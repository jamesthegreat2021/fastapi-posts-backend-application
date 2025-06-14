"""added a column in posts table

Revision ID: bb714585f1ea
Revises: 
Create Date: 2025-06-13 16:12:48.846695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb714585f1ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('likes', sa.Column('id', sa.Integer,nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('likes')
    pass
