import dataclasses
import uuid
from contextlib import (
    asynccontextmanager,
)
from typing import (
    Any,
    AsyncIterator,
)

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
from src.application.dto.photo import (
    PhotoDB,
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
        self._client = s3
        self._repository = photo_repository

    async def upload_file(self, user_id: int, file: UploadFile) -> PhotoUploadResponse:
        filename = f"{user_id}/{uuid.uuid4()}_{file.filename}"

        # noinspection PyArgumentList
        async with self._client.s3_client() as s3:
            await s3.upload_fileobj(file.file, self._client.bucket_name, filename)
        remote_url = (
            f"https://storage.yandexcloud.net/{self._client.bucket_name}/{filename}"
        )
        await self._repository.create(user_id=user_id, remote_url=remote_url)
        return dto.PhotoUploadResponse(remote_url=remote_url)

    async def get_all_photos_from_s3(self, user_id: int) -> list[dict[str, str]]:
        photos = []
        # noinspection PyArgumentList
        async with self._client.get_bucket() as bucket:
            prefix = f"{user_id}/"
            async for obj in bucket.objects.filter(Prefix=prefix):
                filename = obj.key
                remote_url = f"https://storage.yandexcloud.net/{self._client.bucket_name}/{filename}"
                photos.append({"remote_url": remote_url})
        return photos

    async def get_all_photos_from_db(self, user_id: int) -> list[PhotoDB]:
        photos = await self._repository.get_all_photos(user_id=user_id)
        return [PhotoDB(**photo.__dict__) for photo in photos]

    async def update_photo(
            self,
            user_id: int,
            old_photo_url: str,
            new_file: UploadFile
    ) -> PhotoUploadResponse:
        # noinspection PyArgumentList
        async with self._client.s3_client() as s3:
            old_key = old_photo_url.split(f"https://storage.yandexcloud.net/{self._client.bucket_name}/")[1]
            try:
                await s3.get_object(Bucket=self._client.bucket_name, Key=old_key)
            except Exception as e:
                raise ValueError("The specified photo does not exist.") from e

        # noinspection PyArgumentList
        async with self._client.s3_client() as s3:
            await s3.delete_object(Bucket=self._client.bucket_name, Key=old_key)

        return await self.upload_file(user_id, new_file)

    async def delete_photo(
            self,
            photo_url: str
    ) -> None:
        # noinspection PyArgumentList
        async with self._client.s3_client() as s3:
            key = photo_url.split(f"https://storage.yandexcloud.net/{self._client.bucket_name}/")[1]
            try:
                await s3.get_object(Bucket=self._client.bucket_name, Key=key)
            except Exception as e:
                raise ValueError("The specified photo does not exist.") from e

        # noinspection PyArgumentList
        async with self._client.s3_client() as s3:
            await s3.delete_object(Bucket=self._client.bucket_name, Key=key)

    async def get_photo_by_id(self, photo_id: int) -> Any:
        return await self._repository.get(photo_id=photo_id)


"""
user = User(id=1, name="Alice")
task_manager = TaskManager(user)
task = Task(id=1, title="Complete project")
task_manager.add_task(task)
task_manager.get_tasks()
"""
