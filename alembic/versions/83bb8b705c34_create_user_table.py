"""create user table

Revision ID: 83bb8b705c34
Revises: 
Create Date: 2023-02-14 22:51:06.672023

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '83bb8b705c34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=45), nullable=False),
                    sa.Column('email', sa.String(length=45), nullable=False),
                    sa.Column('password', sa.String(length=160), nullable=False),
                    sa.Column('city', sa.String(length=40), nullable=False),
                    sa.Column('photo', sa.String(length=250), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('wall',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('genre_id', sa.String(length=250), nullable=False),
                    sa.Column('datetime', sa.DateTime(), nullable=False),
                    sa.Column('text', sa.String(length=500), nullable=False),
                    sa.Column('photo_wall', sa.String(length=250), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('wall')
    op.drop_table('user')
