"""add user table

Revision ID: e434eba96f5b
Revises: eb9003967868
Create Date: 2023-10-20 23:21:14.031326

"""
from typing import Sequence, Union
from sqlalchemy.sql.sqltypes import TIMESTAMP
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e434eba96f5b'
down_revision: Union[str, None] = 'eb9003967868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
    pass
