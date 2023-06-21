from datetime import datetime
import json
from typing import Dict, List
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import env_config
from backend.helpers.forms import ValidateJsonWithFormBody, form_body
from backend.schemas.file import ImageLink


class CreateSlide(BaseModel):
    name: str = Query(..., max_length=int(
        env_config.get('VITE_MAX_SLIDE_NAME_LENGTH')))
    open_date: datetime
    close_date: datetime | None
    url: str = Query(..., max_length=int(
        env_config.get('VITE_MAX_SLIDE_URL_LENGTH')))
    position: int
    is_active: bool


@form_body
class CreateSlideForm(CreateSlide):
    ...


class Slide(CreateSlide):
    id: int
    picture: ImageLink

    class Config:
        orm_mode = True
