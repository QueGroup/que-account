from typing import (
    Final,
)

import structlog
from structlog import (
    BoundLogger,
)

from .configuration import (
    _configure_default_logging_by_custom,
    _extract_from_record,
)
from .setup import (
    configure_logging,
)

custom_logger: Final[BoundLogger] = structlog.stdlib.get_logger("custom_logger")

__all__ = [
    "custom_logger",
    "configure_logging",
]
