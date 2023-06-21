import re
from pydantic import BaseModel, validator
import phonenumbers
from pydantic.validators import strict_str_validator


class Phone(BaseModel):
    phone: str = None

    @validator("phone")
    def phone_validation(cls, v):
        regex = r"^(+)[1-9][0-9-().]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True


class PhoneNumber(str):
    """Phone Number Pydantic type, using google's phonenumbers"""

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        # Remove spaces
        v = v.strip().replace(' ', '')

        try:
            pn = phonenumbers.parse(v)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('invalid phone number format')

        return cls(phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164))
