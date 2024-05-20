import datetime
from typing import (
    Annotated,
)

from sqlalchemy import (
    func,
)
from sqlalchemy.dialects.postgresql import (
    TIMESTAMP,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]


class Model(DeclarativeBase):
    __abstract__ = True

    id: Mapped[intpk]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
