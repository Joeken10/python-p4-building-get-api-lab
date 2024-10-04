"""Add created_at and updated_at columns to baked_goods

Revision ID: bc29581f2cba
Revises: f67c26f2bda6
Create Date: 2024-10-04 23:55:46.908471
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'bc29581f2cba'
down_revision = 'f67c26f2bda6'
branch_labels = None
depends_on = None


def upgrade():
    # Add created_at and updated_at columns to baked_goods table
    op.add_column('baked_goods', sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=False))
    op.add_column('baked_goods', sa.Column('updated_at', sa.DateTime(), server_default=func.now(), onupdate=func.now(), nullable=False))
    
    # Add bakery_id column and create foreign key constraint
    op.add_column('baked_goods', sa.Column('bakery_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_baked_goods_bakery', 'baked_goods', 'bakeries', ['bakery_id'], ['id'])
    
    # Ensure name column in bakeries is not nullable
    op.alter_column('bakeries', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)


def downgrade():
    # Revert name column in bakeries to nullable
    op.alter_column('bakeries', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # Drop foreign key constraint and the bakery_id column from baked_goods
    op.drop_constraint('fk_baked_goods_bakery', 'baked_goods', type_='foreignkey')
    op.drop_column('baked_goods', 'bakery_id')

    # Drop created_at and updated_at columns from baked_goods
    op.drop_column('baked_goods', 'updated_at')
    op.drop_column('baked_goods', 'created_at')
