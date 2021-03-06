"""Removed the authenticated column

Revision ID: 661ef2aa7fee
Revises: ecd80383e932
Create Date: 2020-05-08 16:26:19.426372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '661ef2aa7fee'
down_revision = 'ecd80383e932'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'authenticated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('authenticated', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
