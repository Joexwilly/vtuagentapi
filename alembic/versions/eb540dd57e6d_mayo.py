"""mayo

Revision ID: eb540dd57e6d
Revises: 7c40e5c9972f
Create Date: 2023-03-19 11:35:55.900818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb540dd57e6d'
down_revision = '7c40e5c9972f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    #update phone number coloumn in users table to string
    op.alter_column('user', 'phone', type_=sa.String)
   


def downgrade() -> None:
    # downgrade phone number coloumn in users table to integer
    op.alter_column('user', 'phone', type_=sa.Integer)
   
