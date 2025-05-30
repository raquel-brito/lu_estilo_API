"""create users table

Revision ID: 2ec7eb25b7a8
Revises: f1a461052aae
Create Date: 2025-05-23 04:51:58.507237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ec7eb25b7a8'
down_revision: Union[str, None] = 'f1a461052aae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('cpf', sa.String(length=14), nullable=True),
    )

def downgrade() -> None:
    pass