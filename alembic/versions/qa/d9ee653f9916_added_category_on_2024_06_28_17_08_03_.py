"""
added category on 2024-06-28 17:08:03.821398

Revision ID: d9ee653f9916
Revises: 86652cb46652
Create Date: 2024-06-28 17:08:04.090923

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d9ee653f9916"
down_revision: Union[str, None] = "86652cb46652"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("todos", sa.Column("category", sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("todos", "category")
    # ### end Alembic commands ###
