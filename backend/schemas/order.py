from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, root_validator
from backend.helpers.forms import form_body
from backend.models.order import OrderStatus
from backend.schemas.product import Product
from backend.schemas.user import UserInfo


class CreateOrderProduct(BaseModel):
    product_id: int
    quantity: int


class DeliveryType(BaseModel):

    market_id: int = Query(default=False, description="ID магазина")
    delivery_address_id: int = Query(
        default=False, description="ID адреса доставки")


class CreateOrder(DeliveryType):
    products: List[CreateOrderProduct]
    market_id: int = None
    delivery_address_id: int = None
    stocks: List[int] = []


class OrderProduct(BaseModel):
    id: UUID
    name: str
    quantity: int
    price: int
    product_id: int
    product: Product

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: UUID
    user_id: int
    status: OrderStatus
    time_created: datetime
    total_price: int
    market_id: int | None
    delivery_address_id: int | None
    order_products: List[OrderProduct]

    class Config:
        orm_mode = True
        use_enum_values = True


class CreateOrderMessage(BaseModel):
    message: str


class OrderMessage(CreateOrderMessage):
    id: UUID
    time_created: datetime
    order_id: UUID
    time_updated: datetime | None
    user: UserInfo

    class Config:
        orm_mode = True
