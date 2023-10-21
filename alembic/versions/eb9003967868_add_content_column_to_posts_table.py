"""add content column to posts table

Revision ID: eb9003967868
Revises: 70916a60f250
Create Date: 2023-10-20 23:11:36.338187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb9003967868'
down_revision: Union[str, None] = '70916a60f250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False)) ###we add a colum to an existing posts table 
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content') ##for every column we add to an eisting table, we must define the drop. just incase we want to revert an action 
    pass
