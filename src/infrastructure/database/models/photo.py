from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from . import (
    models,
)

if TYPE_CHECKING:
    pass


class PhotoModel(models.Model):
    __tablename__ = "profiles"

    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    # user: Mapped["User"] = relationship("User", backref=backref("photos", lazy=True))
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
