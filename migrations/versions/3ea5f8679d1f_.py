"""empty message

Revision ID: 3ea5f8679d1f
Revises: 0b1ba70180fc
Create Date: 2020-08-10 05:26:06.440902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ea5f8679d1f'
down_revision = '0b1ba70180fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author_id', sa.Integer(), nullable=False))
    op.add_column('books', sa.Column('category_id', sa.Integer(), nullable=False))
    op.drop_constraint('books_author_fkey', 'books', type_='foreignkey')
    op.drop_constraint('books_category_fkey', 'books', type_='foreignkey')
    op.create_foreign_key(None, 'books', 'authors', ['author_id'], ['id'])
    op.create_foreign_key(None, 'books', 'categories', ['category_id'], ['id'])
    op.drop_column('books', 'author')
    op.drop_column('books', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('books', sa.Column('author', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.create_foreign_key('books_category_fkey', 'books', 'categories', ['category'], ['id'])
    op.create_foreign_key('books_author_fkey', 'books', 'authors', ['author'], ['id'])
    op.drop_column('books', 'category_id')
    op.drop_column('books', 'author_id')
    # ### end Alembic commands ###