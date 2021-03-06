"""empty message

Revision ID: 22fda6090ace
Revises: 
Create Date: 2018-02-03 03:17:50.521125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22fda6090ace'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes_posts',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('posts_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['posts_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes_posts')
    # ### end Alembic commands ###
