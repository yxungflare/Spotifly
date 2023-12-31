"""for songTable mod nullable

Revision ID: ffa7034207f2
Revises: 99a9bcfde88a
Create Date: 2023-11-28 11:13:13.377891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffa7034207f2'
down_revision: Union[str, None] = '99a9bcfde88a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('song', 'username_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('song', 'playlist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('song', 'playlist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('song', 'username_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
