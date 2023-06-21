import json
from fastapi import Form
from pydantic import BaseModel


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(None) if arg.default is
                        None else Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


class ValidateJsonWithFormBody(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return cls.validate
