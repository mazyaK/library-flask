"""empty message

Revision ID: 0b1ba70180fc
Revises: 736cbc0401da
Create Date: 2020-08-10 05:23:24.586431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1ba70180fc'
down_revision = '736cbc0401da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author', sa.Integer(), nullable=False))
    op.add_column('books', sa.Column('category', sa.Integer(), nullable=False))
    op.drop_constraint('books_category_id_fkey', 'books', type_='foreignkey')
    op.drop_constraint('books_author_id_fkey', 'books', type_='foreignkey')
    op.create_foreign_key(None, 'books', 'authors', ['author'], ['id'])
    op.create_foreign_key(None, 'books', 'categories', ['category'], ['id'])
    op.drop_column('books', 'category_id')
    op.drop_column('books', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('books', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.create_foreign_key('books_author_id_fkey', 'books', 'authors', ['author_id'], ['id'])
    op.create_foreign_key('books_category_id_fkey', 'books', 'categories', ['category_id'], ['id'])
    op.drop_column('books', 'category')
    op.drop_column('books', 'author')
    # ### end Alembic commands ###