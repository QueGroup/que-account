from pydantic import (
    BaseModel,
    ConfigDict,
)


class RoleBaseSchema(BaseModel):
    title: str


class RoleCreateSchema(RoleBaseSchema):
    pass


class RoleUpdateSchema(RoleBaseSchema):
    title: str | None = None


class RoleResponseSchema(RoleBaseSchema):
    role_id: int

    model_config = ConfigDict(from_attributes=True)
