"""first

Revision ID: 4dae63071066
Revises: 
Create Date: 2023-04-02 17:18:14.414452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dae63071066'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('private_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('rental_business_user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('private_id')
    )
    op.create_index(op.f('ix_board_private_id'), 'board', ['private_id'], unique=False)
    op.create_table('customer_user',
    sa.Column('private_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password_encrypted', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('private_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_customer_user_private_id'), 'customer_user', ['private_id'], unique=False)
    op.create_table('rental_business_user',
    sa.Column('private_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password_encrypted', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('private_id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_rental_business_user_private_id'), 'rental_business_user', ['private_id'], unique=False)
    op.create_table('rental_business_user_info',
    sa.Column('private_id', sa.Integer(), nullable=False),
    sa.Column('rental_business_user_id', sa.Integer(), nullable=True),
    sa.Column('business_type', sa.String(), nullable=True),
    sa.Column('business_title', sa.String(), nullable=True),
    sa.Column('business_description', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('private_id'),
    sa.UniqueConstraint('rental_business_user_id')
    )
    op.create_index(op.f('ix_rental_business_user_info_private_id'), 'rental_business_user_info', ['private_id'], unique=False)
    op.create_table('rental_business_user_register_account_token',
    sa.Column('private_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('used_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('private_id'),
    sa.UniqueConstraint('token'),
    sa.UniqueConstraint('used_by')
    )
    op.create_index(op.f('ix_rental_business_user_register_account_token_private_id'), 'rental_business_user_register_account_token', ['private_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rental_business_user_register_account_token_private_id'), table_name='rental_business_user_register_account_token')
    op.drop_table('rental_business_user_register_account_token')
    op.drop_index(op.f('ix_rental_business_user_info_private_id'), table_name='rental_business_user_info')
    op.drop_table('rental_business_user_info')
    op.drop_index(op.f('ix_rental_business_user_private_id'), table_name='rental_business_user')
    op.drop_table('rental_business_user')
    op.drop_index(op.f('ix_customer_user_private_id'), table_name='customer_user')
    op.drop_table('customer_user')
    op.drop_index(op.f('ix_board_private_id'), table_name='board')
    op.drop_table('board')
    # ### end Alembic commands ###
