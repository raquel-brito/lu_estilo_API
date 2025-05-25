"""create users, clients and products tables

Revision ID: fa3f6f1dce6d
Revises: c80705ad622b
Create Date: 2025-05-25 01:01:30.729031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa3f6f1dce6d'
down_revision: Union[str, None] = 'c80705ad622b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column('is_admin', sa.Boolean, server_default=sa.false(), nullable=False),
    )

    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('cpf', sa.String, unique=True, nullable=False),
    )

    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('barcode', sa.String, unique=True, nullable=False),
        sa.Column('section', sa.String, nullable=False),
        sa.Column('stock', sa.Integer, server_default='0', nullable=False),
        sa.Column('expiration_date', sa.Date, nullable=True),
        sa.Column('available', sa.Boolean, server_default=sa.true(), nullable=False),
        sa.Column('image_url', sa.String, nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
