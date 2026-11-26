from uuid import UUID

from fastapi import APIRouter, Response

from app.schemas.object_types import ObjectTypeCreate, ObjectTypeResponse, ObjectTypeUpdate
from app.services import object_types
from app.storage.memory import list_object_types

router = APIRouter(prefix="/object-types", tags=["Object types"])


@router.post("", response_model=ObjectTypeResponse, status_code=201)
async def create_object_type(data: ObjectTypeCreate):
    return object_types.create_object_type(data)


@router.get("", response_model=list[ObjectTypeResponse])
async def get_object_types():
    return list_object_types()


@router.get("/{object_type_id}", response_model=ObjectTypeResponse)
async def get_object_type(object_type_id: UUID):
    return object_types.get_object_type(object_type_id)


@router.patch("/{object_type_id}", response_model=ObjectTypeResponse)
async def update_object_type(object_type_id: UUID, data: ObjectTypeUpdate):
    return object_types.update_object_type(object_type_id, data)


@router.delete("/{object_type_id}", status_code=204)
async def delete_object_type(object_type_id: UUID):
    object_types.delete_object_type(object_type_id)
    return Response(status_code=204)
