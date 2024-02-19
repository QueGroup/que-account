from typing import Final

from .config import (
    Config,
    load_config,
)

config: Final[Config] = load_config()

__all__ = (
    "config",
)
