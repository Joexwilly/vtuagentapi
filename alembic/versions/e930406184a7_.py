"""empty message

Revision ID: e930406184a7
Revises: 
Create Date: 2023-03-31 16:55:23.967019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e930406184a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('wallet', sa.BigInteger()))



def downgrade() -> None:
    op.drop_column('user', 'wallet')


