"""Initial migrate

Revision ID: 3600e26e46b3
Revises: 
Create Date: 2023-11-20 10:42:09.282107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3600e26e46b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('instructor', sa.String(), nullable=True),
    sa.Column('credits', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_course_table'))
    )
    op.create_table('student_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fname', sa.String(), nullable=True),
    sa.Column('lname', sa.String(), nullable=True),
    sa.Column('grad_year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_student_table'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_table')
    op.drop_table('course_table')
    # ### end Alembic commands ###