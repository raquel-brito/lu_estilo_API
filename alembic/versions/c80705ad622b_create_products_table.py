"""create products table

Revision ID: c80705ad622b
Revises: 4dbca50647c7
Create Date: 2025-05-25 00:52:36.787575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c80705ad622b'
down_revision: Union[str, None] = '4dbca50647c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True, nullable=False),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False),
    )
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, unique=True, index=True, nullable=False),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('cpf', sa.String, unique=True, index=True, nullable=False),
    )
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('barcode', sa.String, unique=True, nullable=False),
        sa.Column('section', sa.String, nullable=False),
        sa.Column('stock', sa.Integer, default=0),
        sa.Column('expiration_date', sa.Date, nullable=True),
        sa.Column('available', sa.Boolean, default=True),
        sa.Column('image_url', sa.String, nullable=True),
    )
    
def downgrade():
    op.drop_table('products')
    op.drop_table('clients')
    op.drop_table('users')