from pydantic import BaseModel, validator
from typing import List
from backend.schemas.product import CatalogProduct
from backend.schemas.stock import Stock


class ProductQuantity(BaseModel):
    cart_product_id: int
    product: CatalogProduct
    quantity: int
    is_available: bool

    class Config:
        orm_mode = True


class StockQuantity(BaseModel):
    cart_stock_id: int
    stock: Stock
    quantity: int
    is_available: bool

    class Config:
        orm_mode = True


class CartInfo(BaseModel):
    products: List[ProductQuantity]
    stocks: List[StockQuantity]
    total_price: int

    class Config:
        orm_mode = True
