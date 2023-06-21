from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class ProductAvailability(Base):
    __tablename__ = 'product_availability'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship(
        "Product", foreign_keys=[product_id],
        backref=backref(
            "product_availability", cascade="all,delete"
        )
    )
    market_id = Column(Integer, ForeignKey('markets.id'), nullable=False)
    market = relationship(
        "Market", foreign_keys=[market_id],
        backref=backref(
            "product_availability", cascade="all,delete"
        )
    )
    quantity = Column(Integer, nullable=False)
