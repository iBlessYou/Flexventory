from uuid import UUID

from fastapi import APIRouter, Response

from app.schemas.records import RecordCreate, RecordResponse, RecordUpdate
from app.services import records

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("", response_model=RecordResponse, status_code=201)
async def create_record(data: RecordCreate):
    return records.create_record(data)


@router.get("", response_model=list[RecordResponse])
async def list_records(object_type_id: UUID | None = None):
    return records.list_records(object_type_id)


@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(record_id: UUID):
    return records.get_record(record_id)


@router.patch("/{record_id}", response_model=RecordResponse)
async def update_record(record_id: UUID, data: RecordUpdate):
    return records.update_record(record_id, data)


@router.delete("/{record_id}", status_code=204)
async def delete_record(record_id: UUID):
    records.delete_record(record_id)
    return Response(status_code=204)
