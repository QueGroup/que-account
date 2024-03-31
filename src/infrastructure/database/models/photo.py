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


class PhotoModel(Base):
    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'), nullable=False)
    user = relationship('User', backref=backref('photos', lazy=True))
    photo_url: Mapped[str] = mapped_column(String, nullable=False)
