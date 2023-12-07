"""Adicionar coluna full_name

Revision ID: ad224dbed6c5
Revises: 
Create Date: 2023-12-07 13:23:16.564099

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ad224dbed6c5'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Adiciona a coluna full_name se ainda não existir
    with op.batch_alter_table('user', schema=None) as batch_op:
        if 'full_name' not in op.get_context().get_current_column():
            op.add_column('user', sa.Column('full_name', sa.String(length=100), nullable=True))

def downgrade():
    # Remova a coluna full_name durante a operação de downgrade, se necessário
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('full_name')