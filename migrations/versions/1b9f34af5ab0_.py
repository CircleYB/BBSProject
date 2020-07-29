"""empty message

Revision ID: 1b9f34af5ab0
Revises: 
Create Date: 2020-07-29 01:41:11.298751

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1b9f34af5ab0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    m_thread = op.create_table('m_thread',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('t_post',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('post_time', sa.DateTime(), nullable=False),
                    sa.Column('poster_name', sa.Text(), nullable=True),
                    sa.Column('poster_id', sa.Text(), nullable=True),
                    sa.Column('post_contents', sa.Text(), nullable=True),
                    sa.Column('parent_post_id', sa.Integer(), nullable=True),
                    sa.Column('password', sa.Text(), nullable=True),
                    sa.Column('ke_id', sa.Integer(), nullable=True),
                    sa.Column('is_delete', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['ke_id'], ['m_thread.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('t_good_number',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('poster_id', sa.Integer(), nullable=False),
                    sa.Column('remote_host', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(['poster_id'], ['t_post.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###

    op.bulk_insert(m_thread,
                   [
                       {'id': 0, 'name': '全て'},
                       {'id': 1, 'name': '乾為天'},
                       {'id': 2, 'name': '坤為地'},
                       {'id': 3, 'name': '水雷屯'},
                       {'id': 4, 'name': '山水蒙'},
                       {'id': 5, 'name': '水天需'},
                       {'id': 6, 'name': '天水訟'},
                       {'id': 7, 'name': '地水師'},
                       {'id': 8, 'name': '水地比'},
                       {'id': 9, 'name': '風天小畜'},
                       {'id': 10, 'name': '天沢履'},
                       {'id': 11, 'name': '地天泰'},
                       {'id': 12, 'name': '天地否'},
                       {'id': 13, 'name': '天火同人'},
                       {'id': 14, 'name': '火天大有'},
                       {'id': 15, 'name': '地山謙'},
                       {'id': 16, 'name': '雷地豫'},
                       {'id': 17, 'name': '沢雷随'},
                       {'id': 18, 'name': '山風蠱'},
                       {'id': 19, 'name': '地沢臨'},
                       {'id': 20, 'name': '風地観'},
                       {'id': 21, 'name': '火雷噬嗑'},
                       {'id': 22, 'name': '山火賁'},
                       {'id': 23, 'name': '山地剥'},
                       {'id': 24, 'name': '地雷復'},
                       {'id': 25, 'name': '天雷无妄'},
                       {'id': 26, 'name': '山天大畜'},
                       {'id': 27, 'name': '山雷頤'},
                       {'id': 28, 'name': '沢風大過'},
                       {'id': 29, 'name': '坎為水'},
                       {'id': 30, 'name': '離為火'},
                       {'id': 31, 'name': '沢山咸'},
                       {'id': 32, 'name': '雷風恒'},
                       {'id': 33, 'name': '天山遯'},
                       {'id': 34, 'name': '雷天大壮'},
                       {'id': 35, 'name': '火地晋'},
                       {'id': 36, 'name': '地火明夷'},
                       {'id': 37, 'name': '風火家人'},
                       {'id': 38, 'name': '火沢睽'},
                       {'id': 39, 'name': '水山蹇'},
                       {'id': 40, 'name': '雷水解'},
                       {'id': 41, 'name': '山沢損'},
                       {'id': 42, 'name': '風雷益'},
                       {'id': 43, 'name': '沢天夬'},
                       {'id': 44, 'name': '天風姤'},
                       {'id': 45, 'name': '沢地萃'},
                       {'id': 46, 'name': '地風升'},
                       {'id': 47, 'name': '沢水困'},
                       {'id': 48, 'name': '水風井'},
                       {'id': 49, 'name': '沢火革'},
                       {'id': 50, 'name': '火風鼎'},
                       {'id': 51, 'name': '震為雷'},
                       {'id': 52, 'name': '艮為山'},
                       {'id': 53, 'name': '風山漸'},
                       {'id': 54, 'name': '雷沢帰妹'},
                       {'id': 55, 'name': '雷火豊'},
                       {'id': 56, 'name': '火山旅'},
                       {'id': 57, 'name': '巽為風'},
                       {'id': 58, 'name': '兌為沢'},
                       {'id': 59, 'name': '風水渙'},
                       {'id': 60, 'name': '水沢節'},
                       {'id': 61, 'name': '風沢中孚'},
                       {'id': 62, 'name': '雷山小過'},
                       {'id': 63, 'name': '水火既済'},
                       {'id': 64, 'name': '火水未済'}
                   ]
                   )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_good_number')
    op.drop_table('t_post')
    op.drop_table('m_thread')
    # ### end Alembic commands ###