from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class UserRole(StrEnum):
    viewer = "viewer"
    editor = "editor"
    admin = "admin"


class UserCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username", mode="before")
    @classmethod
    def trim_username(cls, value):
        return value.strip() if isinstance(value, str) else value


class UserSignIn(UserCredentials):
    password: str


class UserRoleUpdate(BaseModel):
    role: UserRole


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole
