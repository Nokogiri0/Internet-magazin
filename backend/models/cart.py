from backend.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class CartProduct(Base):
    __tablename__ = 'cart_products'
    cart_product_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship(
        "Product", foreign_keys=[product_id],
        backref=backref(
            "cart_products", cascade="all,delete"
        )
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    @property
    def is_available(self):
        try:
            return sum([availability.quantity for availability in self.product.available]) > 0
        except Exception as e:
            print(e)


class CartStock(Base):
    __tablename__ = 'cart_stocks'
    cart_stock_id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    stock = relationship(
        "Stock", foreign_keys=[stock_id],
        backref=backref(
            "cart_stocks", cascade="all,delete"
        )
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    @property
    def is_available(self):
        try:
            stock_products = self.stock.products
            stock_availability = 0
            for stock_product in stock_products:
                if len([availability for availability in stock_product.product.available if availability.quantity > 0]) > 0:
                    stock_availability += 1
            return stock_availability == len(stock_products)
        except Exception as e:
            print(e)
