import datetime
from typing import (
    Any,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

__all__ = (
    "Message",
    "SendMessageResponse",
)


class Message(BaseModel):
    message_id: int
    from_: dict[str, Any]
    chat: dict[str, Any]
    date: int
    text: str


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message = Field(None, alias='result')
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            datetime.datetime: lambda x: x.isoformat()
        }
    )
