from uuid import UUID, uuid4

from fastapi import HTTPException

from app.models.object_types import ObjectType
from app.schemas.object_types import ObjectTypeCreate, ObjectTypeUpdate
from app.storage import memory


def get_object_type(object_type_id: UUID) -> ObjectType:
    object_type = memory.get_object_type(object_type_id)
    if object_type is None:
        raise HTTPException(404, "Object type not found")
    return object_type


def check_name(name: str, object_type_id: UUID | None = None):
    existing = memory.find_object_type(name)
    if existing is not None and existing.id != object_type_id:
        raise HTTPException(409, "Object type name already exists")


def check_parent(parent_id: UUID | None, object_type_id: UUID | None = None):
    while parent_id is not None:
        if parent_id == object_type_id:
            raise HTTPException(409, "Object type hierarchy cannot contain cycles")
        parent_id = get_object_type(parent_id).parent_id


def create_object_type(data: ObjectTypeCreate) -> ObjectType:
    check_name(data.name)
    check_parent(data.parent_id)
    return memory.save_object_type(ObjectType(uuid4(), data.name, data.instance_schema, data.parent_id))


def update_object_type(object_type_id: UUID, data: ObjectTypeUpdate) -> ObjectType:
    object_type = get_object_type(object_type_id)
    changes = data.model_dump(exclude_unset=True)
    check_name(changes.get("name", object_type.name), object_type_id)
    check_parent(changes.get("parent_id", object_type.parent_id), object_type_id)
    for field, value in changes.items():
        setattr(object_type, field, value)
    return memory.save_object_type(object_type)


def delete_object_type(object_type_id: UUID):
    get_object_type(object_type_id)
    if any(item.parent_id == object_type_id for item in memory.list_object_types()):
        raise HTTPException(409, "Move or delete child object types first")
    memory.delete_object_type(object_type_id)
