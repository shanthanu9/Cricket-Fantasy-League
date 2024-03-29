"""Added lots of tables

Revision ID: 1a068f69755c
Revises: 
Create Date: 2019-10-30 00:41:20.824816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a068f69755c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batting',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player', sa.String(length=64), nullable=True),
    sa.Column('span', sa.String(length=10), nullable=True),
    sa.Column('matches', sa.String(length=6), nullable=True),
    sa.Column('innings', sa.String(length=6), nullable=True),
    sa.Column('no', sa.String(length=6), nullable=True),
    sa.Column('runs', sa.String(length=6), nullable=True),
    sa.Column('hs', sa.String(length=6), nullable=True),
    sa.Column('ave', sa.String(length=6), nullable=True),
    sa.Column('bf', sa.String(length=6), nullable=True),
    sa.Column('sr', sa.String(length=6), nullable=True),
    sa.Column('hundreds', sa.String(length=6), nullable=True),
    sa.Column('fifties', sa.String(length=6), nullable=True),
    sa.Column('ducks', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bowling',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player', sa.String(length=64), nullable=True),
    sa.Column('span', sa.String(length=10), nullable=True),
    sa.Column('matches', sa.String(length=6), nullable=True),
    sa.Column('innings', sa.String(length=6), nullable=True),
    sa.Column('balls', sa.String(length=6), nullable=True),
    sa.Column('runs', sa.String(length=6), nullable=True),
    sa.Column('wickets', sa.String(length=6), nullable=True),
    sa.Column('best', sa.String(length=6), nullable=True),
    sa.Column('ave', sa.String(length=6), nullable=True),
    sa.Column('econ', sa.String(length=6), nullable=True),
    sa.Column('sr', sa.String(length=6), nullable=True),
    sa.Column('four', sa.String(length=6), nullable=True),
    sa.Column('five', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fielding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player', sa.String(length=64), nullable=True),
    sa.Column('span', sa.String(length=10), nullable=True),
    sa.Column('dismissals', sa.String(length=6), nullable=True),
    sa.Column('catches', sa.String(length=6), nullable=True),
    sa.Column('stumpings', sa.String(length=6), nullable=True),
    sa.Column('catch_wk', sa.String(length=6), nullable=True),
    sa.Column('catch_fi', sa.String(length=6), nullable=True),
    sa.Column('best', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('match_id', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('fielding')
    op.drop_table('bowling')
    op.drop_table('batting')
    # ### end Alembic commands ###
