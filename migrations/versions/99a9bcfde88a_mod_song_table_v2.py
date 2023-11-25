"""Mod Song table v2

Revision ID: 99a9bcfde88a
Revises: ae58f1f47c98
Create Date: 2023-11-25 10:40:08.024234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a9bcfde88a'
down_revision: Union[str, None] = 'ae58f1f47c98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'song_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('song_path', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
