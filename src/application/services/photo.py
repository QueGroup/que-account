from contextlib import (
    asynccontextmanager,
)
import dataclasses
from typing import (
    Any,
    AsyncIterator,
)
import uuid

import aioboto3
from fastapi import (
    UploadFile,
)

from src.application import (
    dto,
)
from src.application.dto import (
    PhotoUploadResponse,
)
from src.infrastructure.database.repositories import (
    PhotoRepository,
)


@dataclasses.dataclass
class S3Storage:
    service_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str
    region_name: str
    bucket_name: str

    @asynccontextmanager
    async def get_bucket(self) -> AsyncIterator[Any]:
        session = aioboto3.Session()
        async with session.resource(
                service_name=self.service_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                region_name=self.region_name
        ) as s3:
            bucket = await s3.Bucket(
                self.bucket_name
            )
            yield bucket

    @asynccontextmanager
    async def s3_client(self) -> AsyncIterator[Any]:
        session = aioboto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        async with session.client(service_name=self.service_name, endpoint_url=self.endpoint_url) as client:
            yield client


class PhotoService:
    def __init__(self, s3: S3Storage, photo_repository: PhotoRepository) -> None:
        self.client = s3
        self.repository = photo_repository

    async def upload_file(self, user_id: int, file: UploadFile) -> PhotoUploadResponse:
        filename = f"{user_id}/{uuid.uuid4()}_{file.filename}"
        # noinspection PyArgumentList
        async with self.client.s3_client() as s3:
            await s3.upload_fileobj(file.file, self.client.bucket_name, filename)
        remote_url = (
            f"https://storage.yandexcloud.net/{self.client.bucket_name}/{filename}"
        )
        await self.repository.create(user_id=user_id, remote_url=remote_url)
        return dto.PhotoUploadResponse(filename=filename, remote_url=remote_url)

    async def get_all_photos(self, user_id: int) -> list[dict[str, str]]:
        photos = []
        # noinspection PyArgumentList
        async with self.client.get_bucket() as bucket:
            prefix = f"{user_id}/"
            async for obj in bucket.objects.filter(Prefix=prefix):
                filename = obj.key
                remote_url = f"https://storage.yandexcloud.net/{self.client.bucket_name}/{filename}"
                photos.append({"remote_url": remote_url})
        return photos
