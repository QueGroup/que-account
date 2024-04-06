from dataclasses import (
    dataclass,
)
from typing import (
    ClassVar,
)


@dataclass(eq=False)
class AppException(Exception):
    """Model Exception"""

    status: ClassVar[int] = 500

    @property
    def title(self) -> str:
        return "An app error occurred"


class DomainException(AppException):
    """Model Domain Exception"""

    @property
    def title(self) -> str:
        return "A domain error occurred"
