"""Adding Token Table

Revision ID: e3913335b0f6
Revises: 792430cd18ef
Create Date: 2023-04-16 18:07:23.569091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3913335b0f6'
down_revision = '792430cd18ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_token_id'), 'token', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_id'), table_name='token')
    op.drop_table('token')
    # ### end Alembic commands ###
