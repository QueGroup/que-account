import datetime

from sqlalchemy import (
    BIGINT,
    TIMESTAMP,
    Boolean,
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

from . import (
    models,
)
from .role import (
    Role,
    roles_to_user,
)


class User(models.Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True, unique=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmation_code: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=true())
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=false())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    language: Mapped[str] = mapped_column(String(2), default=text("'ru'"))

    logins: Mapped["UserLoginModel"] = relationship(
        "UserLoginModel",
        back_populates="user",
        lazy="selectin",
    )
    roles: Mapped[list["Role"]] = relationship(
        secondary=roles_to_user,
        back_populates="users",
        lazy="selectin",
    )
    # photos: Mapped["PhotoModel"] = relationship(
    #     "PhotoModel", backref="user", lazy=True
    # )


class UserLoginModel(models.Model):
    __tablename__ = "user_logins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="logins")
    ip_address: Mapped[str] = mapped_column(String(128))
    user_agent: Mapped[str] = mapped_column(String(256))
