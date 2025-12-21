"""Add cascade behavior to location foreign key

Revision ID: 003
Revises: 002
Create Date: 2025-12-21 16:00:00.000000
App Version: 0.4.2

"""
from alembic import op
import sqlalchemy as sa


revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('fk_observations_location_id', 'observations', type_='foreignkey')
    op.create_foreign_key('fk_observations_location_id', 'observations', 'locations', ['location_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint('fk_observations_location_id', 'observations', type_='foreignkey')
    op.create_foreign_key('fk_observations_location_id', 'observations', 'locations', ['location_id'], ['id'])
