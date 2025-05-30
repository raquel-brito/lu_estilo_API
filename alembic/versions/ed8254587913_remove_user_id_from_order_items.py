"""remove user_id from order_items

Revision ID: ed8254587913
Revises: 1d00b4be8219
Create Date: 2025-05-25 04:37:54.334211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed8254587913'
down_revision: Union[str, None] = '1d00b4be8219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('order_items_user_id_fkey'), 'order_items', type_='foreignkey')
    op.drop_column('order_items', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('order_items_user_id_fkey'), 'order_items', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
