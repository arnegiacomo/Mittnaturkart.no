"""Add user ownership to observations and locations

Revision ID: 007
Revises: 006
Create Date: 2025-12-22 10:00:00.000000
App Version: 0.8.0

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('observations', sa.Column('user_id', UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('fk_observations_user_id', 'observations', 'users', ['user_id'], ['id'])

    op.add_column('locations', sa.Column('user_id', UUID(as_uuid=True), nullable=False))
    op.create_foreign_key('fk_locations_user_id', 'locations', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_locations_user_id', 'locations', type_='foreignkey')
    op.drop_column('locations', 'user_id')

    op.drop_constraint('fk_observations_user_id', 'observations', type_='foreignkey')
    op.drop_column('observations', 'user_id')
