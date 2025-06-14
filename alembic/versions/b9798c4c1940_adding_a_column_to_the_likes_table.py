"""adding a column to the likes table

Revision ID: b9798c4c1940
Revises: bb714585f1ea
Create Date: 2025-06-13 18:09:03.433752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9798c4c1940'
down_revision: Union[str, None] = 'bb714585f1ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('likes',sa.Column('content', sa.String(),nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('likes','content')
    pass
