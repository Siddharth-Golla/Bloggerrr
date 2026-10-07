"""Add roles and user verification

Revision ID: b35565f0aa2e
Revises: 90ec86516e8c
Create Date: 2026-10-06 18:27:00.742121
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b35565f0aa2e"
down_revision: Union[str, Sequence[str], None] = "90ec86516e8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Create roles table.
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    # 2. Create the initial application roles.
    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("id", sa.Integer()),
            sa.column("name", sa.String(length=50)),
        ),
        [
            {"id": 1, "name": "Member"},
            {"id": 2, "name": "Moderator"},
            {"id": 3, "name": "Administrator"},
        ],
    )

    # 3. Add role_id temporarily as nullable so existing users
    # can be migrated safely.
    op.add_column(
        "users",
        sa.Column("role_id", sa.Integer(), nullable=True),
    )

    # 4. Existing and newly created users start as unverified.
    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    # 5. Existing users become Members.
    op.execute(
        sa.text(
            "UPDATE users SET role_id = 1 WHERE role_id IS NULL"
        )
    )

    # 6. SQLite does not support adding a foreign key directly
    # with ALTER TABLE, so use Alembic batch mode.
    #
    # The batch operation recreates the users table with the
    # required constraint and final column definition.
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_foreign_key(
            "fk_users_role_id_roles",
            "roles",
            ["role_id"],
            ["id"],
        )

        batch_op.alter_column(
            "role_id",
            existing_type=sa.Integer(),
            nullable=False,
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint(
            "fk_users_role_id_roles",
            type_="foreignkey",
        )
        batch_op.drop_column("is_verified")
        batch_op.drop_column("role_id")

    op.drop_table("roles")

