"""create foreing key between transacton and user another

Revision ID: 826f0fbdc7b8
Revises: c6421bcd2ec9
Create Date: 2024-12-04 16:32:57.388665

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '826f0fbdc7b8'
down_revision: Union[str, None] = 'c6421bcd2ec9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
