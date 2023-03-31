"""empty message

Revision ID: 2a3729fdf8f2
Revises: bf288ac5b512
Create Date: 2023-03-31 17:00:31.406778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3729fdf8f2'
down_revision = 'bf288ac5b512'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('wallet', sa.BigInteger()))



def downgrade() -> None:
    op.drop_column('user', 'wallet')
