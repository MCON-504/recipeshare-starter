"""add password_hash to users

Revision ID: 43ad5c09c5b0
Revises: 3818d8ca13aa
Create Date: 2026-03-25 17:23:05.201503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43ad5c09c5b0'
down_revision = '3818d8ca13aa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password_hash', sa.String(length=256), nullable=True))


def downgrade():
    op.drop_column('users', 'password_hash')
