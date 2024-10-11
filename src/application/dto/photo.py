import datetime

from pydantic import (
    BaseModel,
)


class PhotoDB(BaseModel):
    id: int
    user_id: int
    remote_url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PhotoS3(BaseModel):
    remote_url: str


class PhotoList(BaseModel):
    photos: list[PhotoS3]


class PhotoUploadResponse(BaseModel):
    remote_url: str
