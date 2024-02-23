import datetime
import re

from sqlalchemy import (
    func,
)
from sqlalchemy.dialects.postgresql import (
    TIMESTAMP,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @staticmethod
    def _insert_underscore(class_name: str) -> str:
        return re.sub(r"(?<=.)([A-Z])", r"_\1", class_name)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls._insert_underscore(cls.__name__).lower()

        if name.endswith("y") and name[-2] not in "aeiou":
            pl_name = name[:-1] + "ies"
        elif name.endswith(("s", "x", "z", "sh", "ch")):
            pl_name = name + "es"
        else:
            pl_name = name + "s"
        return pl_name

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp()
    )
