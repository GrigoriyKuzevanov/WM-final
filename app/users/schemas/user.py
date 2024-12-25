from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: str
    last_name: str
    info: str
    role_id: int | None


class UserCreate(schemas.BaseUserCreate):
    name: str
    last_name: str
    info: str | None


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    last_name: str
    info: str | None
