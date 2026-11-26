from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class Record:
    id: UUID
    name: str
    object_type_id: UUID
    data: dict[str, Any]
