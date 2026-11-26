from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RecordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    object_type_id: UUID
    data: dict[str, Any]

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class RecordUpdate(RecordCreate):
    name: str = Field(default=None, min_length=1, max_length=100)
    object_type_id: UUID = Field(default=None)
    data: dict[str, Any] = Field(default=None)

    @model_validator(mode="after")
    def require_changes(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        return self


class RecordResponse(RecordCreate):
    id: UUID
