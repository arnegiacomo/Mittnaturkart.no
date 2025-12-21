"""Add timezone awareness to datetime columns

Revision ID: 004
Revises: 003
Create Date: 2025-12-21 20:00:00.000000
App Version: 0.5.0

"""
from alembic import op
import sqlalchemy as sa


revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Convert observations table datetime columns to timezone-aware
    op.alter_column('observations', 'date',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    postgresql_using='date AT TIME ZONE \'UTC\'')

    op.alter_column('observations', 'created_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')

    op.alter_column('observations', 'updated_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')

    # Convert locations table datetime columns to timezone-aware
    op.alter_column('locations', 'created_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')

    op.alter_column('locations', 'updated_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')


def downgrade() -> None:
    # Reverse changes - remove timezone awareness
    op.alter_column('observations', 'date',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True))

    op.alter_column('observations', 'created_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True))

    op.alter_column('observations', 'updated_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True))

    op.alter_column('locations', 'created_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True))

    op.alter_column('locations', 'updated_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True))
