"""make song favorite

Revision ID: 467d2389b0f2
Revises: 320a99af04f4
Create Date: 2023-12-06 21:59:23.499231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '467d2389b0f2'
down_revision: Union[str, None] = '320a99af04f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('song', 'is_liked',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('song', 'is_liked',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
