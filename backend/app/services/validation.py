from fastapi import HTTPException
from jsonschema import Draft202012Validator, ValidationError
from referencing import Registry
from referencing.exceptions import Unresolvable


def validate_record_data(data: dict, schema: dict, status_code: int = 422):
    try:
        Draft202012Validator(schema, registry=Registry()).validate(data)
    except ValidationError as error:
        raise HTTPException(status_code, {"path": list(error.absolute_path), "message": error.message}) from error
    except (Unresolvable, RecursionError) as error:
        raise HTTPException(status_code, "Schema contains an unresolved or recursive reference") from error
