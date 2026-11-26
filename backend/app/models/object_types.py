from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class ObjectType:
    id: UUID
    name: str
    instance_schema: dict[str, Any]
    parent_id: UUID | None = None
