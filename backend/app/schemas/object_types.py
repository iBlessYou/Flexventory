from typing import Any
from uuid import UUID

from jsonschema import Draft202012Validator, SchemaError
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ObjectTypeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    instance_schema: dict[str, Any]
    parent_id: UUID | None = None

    @field_validator("name", mode="before")
    @classmethod
    def trim_name(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("instance_schema")
    @classmethod
    def validate_schema(cls, value):
        if value.get("type") != "object":
            raise ValueError("Schema root type must be object")
        if value.get("$schema", Draft202012Validator.META_SCHEMA["$id"]) != Draft202012Validator.META_SCHEMA["$id"]:
            raise ValueError("Use JSON Schema draft 2020-12")
        try:
            Draft202012Validator.check_schema(value)
        except SchemaError as error:
            raise ValueError(error.message) from error
        return value


class ObjectTypeUpdate(ObjectTypeCreate):
    name: str = Field(default=None, min_length=1, max_length=100)
    instance_schema: dict[str, Any] = Field(default=None)

    @model_validator(mode="after")
    def require_changes(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        return self


class ObjectTypeResponse(ObjectTypeCreate):
    id: UUID
