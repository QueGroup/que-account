import datetime

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


# TODO: Может переименовать класс в Model, а файл в models. И получать доступ к базову классу с помощью models.Model
class Base(DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
