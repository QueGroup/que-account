from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import (
    Mapped,
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

# TODO: Сделать нормальный класс
roles_to_user = Table(
    "roles_to_user",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id", Integer, ForeignKey("roles.role_id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
)


class RoleModel(Base):
    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        back_populates="roles",
        secondary=roles_to_user,
    )
