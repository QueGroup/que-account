import datetime

from pydantic import (
    BaseModel,
)

# Если нужно будет добавить enum, то нужно в ConfigDict добавить use_enum_values

class ProfileBase(BaseModel):
    first_name: str
    gender: str
    city: str
    latitude: float
    longitude: float
    birthdate: datetime.datetime
    description: str
    interested_in: str
    hobbies: list[str]  # не факт


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(ProfileBase):
    first_name: str | None = None
    gender: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool | None = None
    birthdate: datetime.datetime | None = None
    description: str | None = None
    interested_in: str | None = None
    hobbies: list[str] | None = None
