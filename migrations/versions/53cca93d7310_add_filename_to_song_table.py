"""add filename to song_table

Revision ID: 53cca93d7310
Revises: 467d2389b0f2
Create Date: 2023-12-20 10:46:56.958932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53cca93d7310'
down_revision: Union[str, None] = '467d2389b0f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('filename', sa.String(length=150), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'filename')
    # ### end Alembic commands ###
