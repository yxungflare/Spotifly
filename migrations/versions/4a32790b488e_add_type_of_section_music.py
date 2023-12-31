"""add type of section_music

Revision ID: 4a32790b488e
Revises: 235859b482fd
Create Date: 2023-11-08 09:32:26.028025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a32790b488e'
down_revision: Union[str, None] = '235859b482fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albom', sa.Column('selection_type', sa.String(length=150), nullable=False))
    op.add_column('playlist', sa.Column('selection_type', sa.String(length=150), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('playlist', 'selection_type')
    op.drop_column('albom', 'selection_type')
    # ### end Alembic commands ###
