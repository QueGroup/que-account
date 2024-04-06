from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    BIGINT,
    Date,
    Float,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from . import models

if TYPE_CHECKING:
    pass


class Profile(models.Model):
    __tablename__ = "profiles"

    profile_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(128))
    gender: Mapped[str] = mapped_column(String(2))
    show_me: Mapped[str] = mapped_column(String(2))
    date_of_birth: Mapped[Date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(String(1024))
    country: Mapped[str] = mapped_column(String(32))
    city: Mapped[str] = mapped_column(String(64))
    longitude: Mapped[float] = mapped_column(Float)
