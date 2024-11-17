"""fix username

Revision ID: 60c09320cab3
Revises: 1ec1d7a83235
Create Date: 2024-11-10 16:45:08.623403

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60c09320cab3"
down_revision: Union[str, None] = "1ec1d7a83235"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("username", sa.String(), nullable=True))
    op.drop_constraint("user_usename_key", "user", type_="unique")
    op.create_unique_constraint(None, "user", ["username"])
    op.drop_column("user", "usename")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("usename", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_constraint(None, "user", type_="unique")
    op.create_unique_constraint("user_usename_key", "user", ["usename"])
    op.drop_column("user", "username")
    # ### end Alembic commands ###
