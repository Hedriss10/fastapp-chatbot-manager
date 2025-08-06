"""create finance tables

Revision ID: 41919cbdf07b
Revises:
Create Date: 2025-07-31 21:32:00.020157

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41919cbdf07b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Certifique-se que o schema 'finance' existe
    op.execute("CREATE SCHEMA IF NOT EXISTS finance")

    # Tabela account (sem schema, se for default/public)
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.VARCHAR(200)),
        sa.Column("last_transaction_date", sa.DateTime()),
    )

    # Tabela products no schema 'finance'
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("description", sa.String(length=30), nullable=False),
        sa.Column("value_operation", sa.Numeric(10, 2), server_default="0.00"),
        sa.Column("time_to_spend", sa.Interval, nullable=False),
        sa.Column("commission", sa.Float, server_default="0.0"),
        sa.Column("category", sa.String(length=20)),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("updated_by", sa.Integer),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("deleted_by", sa.Integer),
        sa.Column("is_deleted", sa.Boolean, server_default=sa.text("false")),
        schema="finance",
    )


def downgrade():
    # Dropar tabela do schema 'finance'
    op.drop_table("products", schema="finance")

    # Dropar tabela account do schema padrão
    op.drop_table("account")
