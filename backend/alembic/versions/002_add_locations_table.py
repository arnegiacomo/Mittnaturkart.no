"""Add locations table and update observations

Revision ID: 002
Revises: 001
Create Date: 2025-12-21 12:00:00.000000
App Version: 0.4.2

"""
from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create locations table
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)

    # Add location_id to observations
    op.add_column('observations', sa.Column('location_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_observations_location_id', 'observations', 'locations', ['location_id'], ['id'])

    # Drop latitude and longitude from observations
    op.drop_column('observations', 'latitude')
    op.drop_column('observations', 'longitude')


def downgrade() -> None:
    # Add latitude and longitude back to observations
    op.add_column('observations', sa.Column('latitude', sa.Float(), nullable=False))
    op.add_column('observations', sa.Column('longitude', sa.Float(), nullable=False))

    # Drop foreign key and location_id from observations
    op.drop_constraint('fk_observations_location_id', 'observations', type_='foreignkey')
    op.drop_column('observations', 'location_id')

    # Drop locations table
    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_table('locations')
