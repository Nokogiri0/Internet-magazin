from datetime import datetime
import json
from typing import Dict, List
from pydantic import BaseModel
from fastapi import Query
from backend.core.config import env_config
from backend.helpers.forms import ValidateJsonWithFormBody, form_body
from backend.schemas.file import ImageLink
from backend.schemas.market import MarketInfo
from backend.schemas.catalog import CreatedCategory


class CreateReview(BaseModel):
    description: str = Query(..., min_length=int(env_config.get('VITE_MIN_REVIEW_DESCRIPTION_LENGTH')), max_length=int(env_config.get('VITE_MAX_REVIEW_DESCRIPTION_LENGTH')),
                             description="Description must be between 10 and 255 characters")
    rating: int = Query(..., ge=0, le=10,
                        description="Rating must be between 1 and 10")


class Review(CreateReview):
    id: int
    user_id: int
    time_created: datetime
    product_id: int

    class Config:
        orm_mode = True


class UpdateProductModel(BaseModel):
    name: str
    price: int
    characteristics: Dict[str, str]
    description: str | None


class CreateProductForm(UpdateProductModel, ValidateJsonWithFormBody):
    ...


class UpdateProduct(UpdateProductModel, ValidateJsonWithFormBody):
    ...


class CatalogProduct(UpdateProductModel):
    id: int
    picture: ImageLink
    picture_min: ImageLink

    class Config:
        orm_mode = True


class ProductAvailabilityMarket(MarketInfo):
    quantity: int

    class Config:
        orm_mode = True


class Product(CatalogProduct):
    reviews: List[Review] = []
    my_review: Review | None = None
    orders_count: int
    path: List[CreatedCategory]
    available: List[ProductAvailabilityMarket]

    class Config:
        orm_mode = True


class ProductAvailability(BaseModel):
    product_id: int
    markets: List[ProductAvailabilityMarket] = []


class CreateProductAvailability(BaseModel):

    market_id: int
    quantity: int
