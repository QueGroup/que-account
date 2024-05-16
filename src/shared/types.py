from typing import (
    Any,
    TypeVar,
)

from pydantic import (
    BaseModel,
)

from src.infrastructure.database import (
    models,
)

ModelT = TypeVar("ModelT", bound=models.Model)
CreateSchemaT = TypeVar("CreateSchemaT", bound=Any)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
SchemaT = TypeVar("SchemaT", bound=BaseModel)
