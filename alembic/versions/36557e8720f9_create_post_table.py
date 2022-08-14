"""create post table

Revision ID: 36557e8720f9
Revises: 
Create Date: 2022-08-14 17:55:16.564372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36557e8720f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
