from typing import (
    Annotated,
)

from fastapi import (
    Depends,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.infrastructure.database import (
    db_conn,
)

ISession = Annotated[AsyncSession, Depends(db_conn.get_session)]
