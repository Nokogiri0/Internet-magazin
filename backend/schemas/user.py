from pydantic import BaseModel
from backend.helpers.forms import form_body
from backend.schemas.file import ImageLink
from backend.schemas.suply import PhoneNumber


class UserAuth(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: PhoneNumber | None = None
    username: str


class UserTypes(BaseModel):
    is_superuser: bool = False


class UserWithTypeRegister(UserBase, UserAuth, UserTypes):
    ...


class UserRegister(UserBase, UserAuth):
    ...


class UserModifiable(UserBase):
    ...


class UserInfo(UserTypes, UserBase):
    id: int
    username: str
    picture: ImageLink | None = None

    class Config:
        orm_mode = True


class CreateAddress(BaseModel):
    address: str
    city: str
    zip_code: int
