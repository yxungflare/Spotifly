"""add is_liked status

Revision ID: 9178959d5228
Revises: c07bda57892d
Create Date: 2023-11-24 12:55:23.171215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9178959d5228'
down_revision: Union[str, None] = 'c07bda57892d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlist', sa.Column('is_liked', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('playlist', 'is_liked')
    # ### end Alembic commands ###
