from typing import Final

from src.app import (
    config,
)
from .db_helper import (
    DBConnector,
)

db_conn: Final[DBConnector] = DBConnector(config.db)

__all__ = (
    "db_conn",
)
