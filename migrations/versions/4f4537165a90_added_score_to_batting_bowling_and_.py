"""Added score to batting, bowling and fielding

Revision ID: 4f4537165a90
Revises: 42785503b566
Create Date: 2019-10-30 16:57:52.498478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f4537165a90'
down_revision = '42785503b566'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('batting', sa.Column('score', sa.Float(), nullable=True))
    op.add_column('bowling', sa.Column('score', sa.Float(), nullable=True))
    op.add_column('fielding', sa.Column('score', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fielding', 'score')
    op.drop_column('bowling', 'score')
    op.drop_column('batting', 'score')
    # ### end Alembic commands ###
