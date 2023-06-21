from backend.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum, orm
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from sqlalchemy.orm import backref
from sqlalchemy.sql import func


class OrderStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    cancelled = "cancelled"
    done = "done"


class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref=backref(
        "orders", cascade="all,delete"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    market_id = Column(Integer, ForeignKey('markets.id'))
    delivery_address_id = Column(Integer, ForeignKey('user_addresses.id'))
    delivery_address = relationship(
        "UserAddress", foreign_keys=[delivery_address_id])
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    order_products = relationship(
        "OrderProduct", backref=backref("order", cascade="all,delete"))

    @property
    def total_price(self):
        return sum([product.price * product.quantity for product in self.order_products])


class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey(
        'orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    product = relationship("Product", foreign_keys=[product_id])


class OrderMessage(Base):
    __tablename__ = "order_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey(
        'orders.id'), nullable=False)
    message = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    user = relationship("User", foreign_keys=[user_id])
