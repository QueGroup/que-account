from pydantic import (
    BaseModel,
)


class Photo(BaseModel):
    remote_url: str


class PhotoList(BaseModel):
    photos: list[Photo]


class PhotoUploadResponse(BaseModel):
    filename: str
    remote_url: str
