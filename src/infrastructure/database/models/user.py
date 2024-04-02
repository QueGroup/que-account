import datetime
from typing import (
    TYPE_CHECKING,
)

from sqlalchemy import (
    BIGINT,
    TIMESTAMP,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    false,
    text,
    true,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import (
    Base,
)
from .role import (
    roles_to_user,
)

if TYPE_CHECKING:
    from .role import (
        RoleModel,
    )


class UserModel(Base):
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmation_code: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=true())
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=false())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    language: Mapped[str] = mapped_column(String(2), default=text("'ru'"))

    signature: Mapped["UserSignatureModel"] = relationship(
        "UserSignatureModel",
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )
    logins: Mapped["UserLoginModel"] = relationship(
        "UserLoginModel",
        back_populates="user",
        lazy="selectin",
    )
    refresh_tokens: Mapped["UserRefreshTokenModel"] = relationship(
        "UserRefreshTokenModel",
        back_populates="user",
    )
    roles: Mapped[list["RoleModel"]] = relationship(
        secondary=roles_to_user,
        back_populates="users",
        lazy="selectin",
    )
    # photos: Mapped["PhotoModel"] = relationship(
    #     "PhotoModel", backref="user", lazy=True
    # )


class UserSignatureModel(Base):
    signature: Mapped[str] = mapped_column(String(128), primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="signature")


class UserLoginModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="logins")
    ip_address: Mapped[str] = mapped_column(String(128))
    user_agent: Mapped[str] = mapped_column(String(256))


class UserRefreshTokenModel(Base):
    token: Mapped[str] = mapped_column(String(512), nullable=False, index=True, primary_key=True)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="refresh_tokens")
