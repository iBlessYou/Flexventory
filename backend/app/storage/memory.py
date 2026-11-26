from uuid import UUID

from app.models.users import User
from app.models.records import Record
from app.models.object_types import ObjectType

users: dict[UUID, User] = {}


def find_user(username: str) -> User | None:
    return next((user for user in users.values() if user.username.casefold() == username.casefold()), None)


def get_user(user_id: UUID) -> User | None:
    return users.get(user_id)


def save_user(user: User) -> User:
    users[user.id] = user
    return user


object_types: dict[UUID, ObjectType] = {}


def list_object_types() -> list[ObjectType]:
    return list(object_types.values())


def find_object_type(name: str) -> ObjectType | None:
    return next((item for item in object_types.values() if item.name.casefold() == name.casefold()), None)


def get_object_type(object_type_id: UUID) -> ObjectType | None:
    return object_types.get(object_type_id)


def save_object_type(object_type: ObjectType) -> ObjectType:
    object_types[object_type.id] = object_type
    return object_type


def delete_object_type(object_type_id: UUID):
    del object_types[object_type_id]


records: dict[UUID, Record] = {}


def list_records(object_type_id: UUID | None = None) -> list[Record]:
    return [record for record in records.values() if object_type_id is None or record.object_type_id == object_type_id]


def get_record(record_id: UUID) -> Record | None:
    return records.get(record_id)


def save_record(record: Record) -> Record:
    records[record.id] = record
    return record


def delete_record(record_id: UUID):
    del records[record_id]
