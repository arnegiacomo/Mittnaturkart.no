"""Initial migration - create observations table

Revision ID: 001
Revises:
Create Date: 2025-12-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('observations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('species', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_observations_id'), 'observations', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_observations_id'), table_name='observations')
    op.drop_table('observations')
