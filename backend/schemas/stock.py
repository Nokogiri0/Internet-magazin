from datetime import datetime
from typing import List
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import env_config
from backend.helpers.forms import ValidateJsonWithFormBody
from backend.schemas.file import ImageLink
from backend.schemas.product import Product


class CreateStockProduct(BaseModel):
    product_id: int
    quantity: int
    price: int

    class Config:
        orm_mode = True


class CreateStock(BaseModel):
    name: str = Query(..., min_length=int(env_config.get('VITE_MIN_STOCK_NAME_LENGTH')), max_length=int(env_config.get('VITE_MAX_STOCK_NAME_LENGTH')),
                      description="Name must be between 10 and 255 characters")
    open_date: datetime = Query(...,
                                description="Open date must be in ISO format")
    close_date: datetime = None
    description: str = Query(..., min_length=int(env_config.get('VITE_MIN_STOCK_DESCRIPTION_LENGTH')), max_length=int(env_config.get('VITE_MAX_STOCK_DESCRIPTION_LENGTH')),
                             description="Description must be between 10 and 255 characters")


class CreateStockForm(CreateStock, ValidateJsonWithFormBody):
    products: List[CreateStockProduct] = []


class StockProduct(CreateStockProduct):
    product: Product

    class Config:
        orm_mode = True


class Stock(CreateStock):
    id: int
    picture: ImageLink
    products: List[StockProduct]

    class Config:
        orm_mode = True
