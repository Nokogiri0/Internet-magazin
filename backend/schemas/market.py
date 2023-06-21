from pydantic import BaseModel
from backend.schemas.suply import PhoneNumber
from fastapi import Query
from backend.core.config import env_config


class CreateMarket(BaseModel):
    address: str = Query(..., min_length=int(env_config.get(
        "VITE_MIN_ADDRESS_LENGTH")), max_length=int(env_config.get("VITE_MAX_ADDRESS_LENGTH")))
    phone: PhoneNumber
    description: str = None
    weekday_hours: str
    weekend_hours: str


class MarketInfo(CreateMarket):
    id: int

    class Config:
        orm_mode = True
