from uuid import UUID, uuid4

from fastapi import HTTPException

from app.models.records import Record
from app.schemas.records import RecordCreate, RecordUpdate
from app.services.object_types import get_object_type
from app.services.validation import validate_record_data
from app.storage import memory


def get_record(record_id: UUID) -> Record:
    record = memory.get_record(record_id)
    if record is None:
        raise HTTPException(404, "Record not found")
    return record


def list_records(object_type_id: UUID | None = None) -> list[Record]:
    if object_type_id is not None:
        get_object_type(object_type_id)
    return memory.list_records(object_type_id)


def create_record(data: RecordCreate) -> Record:
    object_type = get_object_type(data.object_type_id)
    validate_record_data(data.data, object_type.instance_schema)
    return memory.save_record(Record(uuid4(), data.name, data.object_type_id, data.data))


def update_record(record_id: UUID, data: RecordUpdate) -> Record:
    record = get_record(record_id)
    changes = data.model_dump(exclude_unset=True)
    object_type = get_object_type(changes.get("object_type_id", record.object_type_id))
    validate_record_data(changes.get("data", record.data), object_type.instance_schema)
    for field, value in changes.items():
        setattr(record, field, value)
    return memory.save_record(record)


def delete_record(record_id: UUID):
    get_record(record_id)
    memory.delete_record(record_id)
