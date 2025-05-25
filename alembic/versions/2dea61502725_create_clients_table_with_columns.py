"""create clients table with columns

Revision ID: 2dea61502725
Revises: 8ce0d559912d
Create Date: 2025-05-25 00:24:02.865010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dea61502725'
down_revision: Union[str, None] = '8ce0d559912d'
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
    """Downgrade schema."""
    pass
