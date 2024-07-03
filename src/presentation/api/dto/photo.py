import datetime

from pydantic import (
    BaseModel,
)


class Photo(BaseModel):
    user_id: int
    remote_url: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PhotosResponse(BaseModel):
    photos: list[Photo]


class PhotoUploadResponse(BaseModel):
    remote_url: str
