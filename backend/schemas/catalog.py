from __future__ import annotations
import json
from typing import Any, Dict, List
from pydantic import BaseModel

from backend.helpers.forms import ValidateJsonWithFormBody, form_body
from backend.schemas.file import ImageLink


class CreateCategoryBase(BaseModel):
    parent_id: int | None
    name: str

    class Config:
        orm_mode = True


class CreateCategory(CreateCategoryBase):
    parent_products_to_child: bool = False


class CreateCategoryForm(CreateCategory):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CategoryInfo(BaseModel):
    name: str


class CreatedCategory(CreateCategoryBase):
    id: int
    picture: ImageLink
    pages: int = 0

    class Config:
        orm_mode = True


class Category(CreatedCategory):
    products: List


class Categories(CreatedCategory):
    children: List[Categories] = []

    class Config:
        orm_mode = True
