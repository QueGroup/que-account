"""initai create

Revision ID: 01a1670187af
Revises: f446d361ddb4
Create Date: 2024-03-01 00:24:01.211423

"""
from typing import (
    Sequence,
    Union,
)

from alembic import (
    op,
)
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "01a1670187af"
down_revision: Union[str, None] = "f446d361ddb4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("telegram_id", sa.BIGINT(), nullable=True))
    op.add_column("users", sa.Column("password", sa.String(length=255), nullable=True))
    op.add_column(
        "users", sa.Column("confirmation_code", sa.String(length=255), nullable=True)
    )
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.add_column("users", sa.Column("is_superuser", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True))
    op.add_column("users", sa.Column("language", sa.String(length=2), nullable=False))
    op.create_unique_constraint(None, "users", ["user_id"])
    op.create_unique_constraint(None, "users", ["telegram_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
    op.drop_column("users", "language")
    op.drop_column("users", "deleted_at")
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_active")
    op.drop_column("users", "confirmation_code")
    op.drop_column("users", "password")
    op.drop_column("users", "telegram_id")
    # ### end Alembic commands ###