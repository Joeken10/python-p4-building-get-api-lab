"""Change price to float in BakedGood

Revision ID: f67c26f2bda6
Revises: 1a660c242acb
Create Date: 2024-10-04 23:39:49.192058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f67c26f2bda6'
down_revision = '1a660c242acb'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'new_baked_goods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),  # Set NOT NULL
        sa.Column('price', sa.Float, nullable=False)  # Assuming price is now float
    )
    
    # Copy data from the old table to the new table
    op.execute(
        'INSERT INTO new_baked_goods (id, name, price) SELECT id, name, price FROM baked_goods'
    )
    
    # Drop the old table
    op.drop_table('baked_goods')
    
    # Rename the new table to the old table's name
    op.rename_table('new_baked_goods', 'baked_goods')

def downgrade():
    # Reverse the upgrade operation if necessary
    op.create_table(
        'old_baked_goods',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),  # Change to allow NULL if needed
        sa.Column('price', sa.Float)  # Revert price to original type
    )
    
    # Copy data back if necessary
    op.execute(
        'INSERT INTO old_baked_goods (id, name, price) SELECT id, name, price FROM baked_goods'
    )
    
    op.drop_table('baked_goods')
    op.rename_table('old_baked_goods', 'baked_goods')
