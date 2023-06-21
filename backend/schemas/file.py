from pydantic import BaseModel
from backend.helpers.images import image_id_to_url
from backend.models.files import Image


class File(BaseModel):
    file_name: str
    user_id: int
    type: str
    url: str
    original_file_name: str


class ImageLink(BaseModel):
    '''convert relationship to image link'''

    @classmethod
    def get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Image):
        if not v:
            return None
        if isinstance(v, str):
            return v
        elif not isinstance(v, Image):
            raise TypeError('ImageLink must be Image (model)')
        return image_id_to_url(v.id)
