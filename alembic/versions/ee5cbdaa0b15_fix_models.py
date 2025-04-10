"""fix models

Revision ID: ee5cbdaa0b15
Revises: b9a740259a9b
Create Date: 2025-03-16 14:43:30.682590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ee5cbdaa0b15'
down_revision: Union[str, None] = 'b9a740259a9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('referral_bonus', 'referrer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('referral_bonus', 'referred_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('referral_bonus', 'amount',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
    op.alter_column('referral_bonus', 'level',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('referral_bonus', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_constraint('referral_bonus_referred_id_fkey', 'referral_bonus', type_='foreignkey')
    op.drop_constraint('referral_bonus_referrer_id_fkey', 'referral_bonus', type_='foreignkey')
    op.create_foreign_key(None, 'referral_bonus', 'users', ['referrer_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'referral_bonus', 'users', ['referred_id'], ['id'], ondelete='CASCADE')
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'balance',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
    op.drop_constraint('users_referrer_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'users', ['referrer_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_referrer_id_fkey', 'users', 'users', ['referrer_id'], ['id'])
    op.alter_column('users', 'balance',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'referral_bonus', type_='foreignkey')
    op.drop_constraint(None, 'referral_bonus', type_='foreignkey')
    op.create_foreign_key('referral_bonus_referrer_id_fkey', 'referral_bonus', 'users', ['referrer_id'], ['id'])
    op.create_foreign_key('referral_bonus_referred_id_fkey', 'referral_bonus', 'users', ['referred_id'], ['id'])
    op.alter_column('referral_bonus', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('referral_bonus', 'level',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('referral_bonus', 'amount',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
    op.alter_column('referral_bonus', 'referred_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('referral_bonus', 'referrer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
