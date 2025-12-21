"""Create keycloak schema

Revision ID: 006
Revises: 005
Create Date: 2025-12-21 20:00:00.000000
App Version: 0.8.0

"""
from alembic import op


revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS keycloak')


def downgrade() -> None:
    op.execute('DROP SCHEMA IF EXISTS keycloak CASCADE')
