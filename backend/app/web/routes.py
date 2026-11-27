from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services import object_types, records
from app.storage import memory

frontend = Path(__file__).resolve().parents[3] / "frontend"
templates = Jinja2Templates(directory=frontend / "template")
templates.env.policies["json.dumps_kwargs"] = {"ensure_ascii": False, "sort_keys": False}
router = APIRouter(include_in_schema=False)


def page(request: Request, template: str, **context):
    return templates.TemplateResponse(request=request, name=template, context=context)


@router.get("/")
async def inventory(request: Request, object_type_id: UUID | None = None):
    selected = object_types.get_object_type(object_type_id) if object_type_id else None
    return page(request, "inventory.html", types=memory.list_object_types(), selected=selected, records=records.list_records(object_type_id))


@router.get("/types/new")
async def new_type(request: Request):
    return page(request, "object_type_form.html", item=None, types=memory.list_object_types())


@router.get("/types/{item_id}/edit")
async def edit_type(request: Request, item_id: UUID):
    item = object_types.get_object_type(item_id)
    return page(request, "object_type_form.html", item=item, types=memory.list_object_types())


@router.get("/records/new")
async def new_record(request: Request, object_type_id: UUID | None = None):
    if object_type_id:
        object_types.get_object_type(object_type_id)
    return page(request, "record_form.html", item=None, selected_id=object_type_id, types=memory.list_object_types())


@router.get("/records/{item_id}")
async def record_detail(request: Request, item_id: UUID):
    item = records.get_record(item_id)
    return page(request, "record_detail.html", item=item, object_type=object_types.get_object_type(item.object_type_id))


@router.get("/records/{item_id}/edit")
async def edit_record(request: Request, item_id: UUID):
    item = records.get_record(item_id)
    return page(request, "record_form.html", item=item, selected_id=item.object_type_id, types=memory.list_object_types())
