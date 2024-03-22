from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import (
    Base,
)

if TYPE_CHECKING:
    pass


class InterestModel(Base):
    interest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
