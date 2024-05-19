import abc

import httpx
from pydantic import (
    BaseModel,
)

from src.application import (
    dto,
)


class Notifier(abc.ABC):
    @abc.abstractmethod
    async def send_message(self, chat_id: int, text: str) -> BaseModel:
        pass


class CompositeNotifier(Notifier):
    def __init__(self) -> None:
        self.notifiers: list[Notifier] = []

    def add_notifier(self, notifier: Notifier) -> None:
        self.notifiers.append(notifier)

    async def send_message(self, chat_id: int, text: str) -> None:
        for notifier in self.notifiers:
            await notifier.send_message(chat_id, text)


class TelegramNotifierService(Notifier):
    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.bot_token}/{method}"

    async def send_message(self, chat_id: int, text: str) -> dto.SendMessageResponse:
        url = self.get_url("sendMessage")
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 403:
                pass
            if response.status_code == 400:
                pass
            else:
                response_dict = response.json()
                result = response_dict["result"]
            return dto.SendMessageResponse(
                ok=response_dict.get("ok"),
                result=dto.Message(
                    message_id=result.get("message_id"),
                    from_=result.get("from"),
                    chat=result.get("chat"),
                    date=result.get("date"),
                    text=result.get("text"),
                ),
            )
