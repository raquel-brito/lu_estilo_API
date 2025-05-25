"""create clients table

Revision ID: 8ce0d559912d
Revises: ce6f2ddf338d
Create Date: 2025-05-25 00:16:15.806015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ce0d559912d'
down_revision: Union[str, None] = 'ce6f2ddf338d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'clients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('cpf', sa.String(length=14), nullable=True),
        # adicione outras colunas que você precisa
    )

def downgrade() -> None:
    op.drop_table('clients')