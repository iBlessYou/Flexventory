from dataclasses import dataclass
from uuid import UUID

from app.schemas.users import UserRole


@dataclass
class User:
    id: UUID
    username: str
    password_hash: bytes
    salt: bytes
    role: UserRole = UserRole.viewer
