from typing import List
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, event, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.orm import backref


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    name = Column(String(
        int(env_config.get('VITE_MAX_STOCK_NAME_LENGTH'))
    ), index=True)
    open_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
    description = Column(
        String(int(env_config.get('VITE_MAX_STOCK_DESCRIPTION_LENGTH'))))
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
        )
    )
    picture = relationship("Image", foreign_keys=[
                           picture_id], cascade="all,delete")
    products = relationship(
        "StockProduct", cascade="all,delete", backref="stock"
    )


class StockProduct(Base):
    __tablename__ = 'stock_products'
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey(
        'stocks.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=True)
    price = Column(Integer, nullable=False)
    product = relationship(
        "Product", foreign_keys=[product_id],
        backref=backref(
            "products", cascade="all,delete"
        )
    )
