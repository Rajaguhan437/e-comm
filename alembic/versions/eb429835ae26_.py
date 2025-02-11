"""empty message

Revision ID: eb429835ae26
Revises: 
Create Date: 2024-11-14 11:46:34.416923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb429835ae26'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sub_category', 'price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sub_category', sa.Column('price', sa.REAL(), server_default=sa.text('0'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
