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
    backref,
    mapped_column,
    relationship,
)

from .base import (
    Base,
)

if TYPE_CHECKING:
    from .user import (
        UserModel,
    )


class PhotoModel(Base):
    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", backref=backref("photos", lazy=True))
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
