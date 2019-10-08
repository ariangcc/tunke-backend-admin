"""empty message

Revision ID: e5c24151988e
Revises: 2fa91c41d8c9
Create Date: 2019-10-08 16:53:58.620583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c24151988e'
down_revision = '2fa91c41d8c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secret_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('secret_question')
    # ### end Alembic commands ###
