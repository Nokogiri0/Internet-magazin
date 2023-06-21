from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from backend.core.config import env_config, settings
from sqlalchemy.dialects.postgresql import UUID
from backend.models.order import Order, OrderProduct, OrderStatus
from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_mptt.mixins import BaseNestedSets
from backend.models.market import Market
from backend.models.availability import ProductAvailability


class Category(Base, BaseNestedSets):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
        )
    )
    picture = relationship("Image", foreign_keys=[
                           picture_id], cascade="all,delete")
    name = Column(String(
        int(
            env_config.get('VITE_MAX_CATEGORY_NAME_LENGTH')
        )
    ), index=True)
    products = relationship(
        "Product", backref="category", passive_deletes=True, cascade="all,delete")

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @property
    def pages(self):
        products_per_page = int(env_config.get('VITE_PRODUCTS_PER_PAGE'))
        return object_session(self).query(Product).filter_by(category_id=self.id).count() // products_per_page + 1


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey(
        'categories.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(
        int(
            env_config.get('VITE_MAX_PRODUCT_NAME_LENGTH')
        )
    ), index=True)
    characteristics = Column(JSON)
    price = Column(Integer, nullable=False)
    description = Column(String)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
            name='products_picture_id_fkey',
            ondelete='SET NULL'
        )
    )
    picture = relationship("Image", foreign_keys=[
                           picture_id], cascade="all,delete")
    picture_min_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
            name='products_picture_min_id_fkey',
            ondelete='SET NULL'
        )
    )
    picture_min = relationship(
        "Image",
        foreign_keys=[
            picture_min_id
        ],
        cascade="all,delete")

    @property
    def orders_count(self):
        return object_session(self).query(OrderProduct).join(Order).filter(Order.status == OrderStatus.done, OrderProduct.product_id == self.id).count()

    @property
    def path(self):
        categories = []
        find_id = self.category_id
        while find_id is not None:
            category = object_session(self).query(
                Category).filter(Category.id == find_id).first()
            find_id = category.parent_id
            categories.append(category)
        return categories[::-1]

    @property
    def available(self):
        return object_session(self).query(
            *Market.__table__.columns,
            ProductAvailability.quantity
        ).join(
            ProductAvailability,
            ProductAvailability.product_id == self.id).filter(ProductAvailability.market_id == Market.id).group_by(Market.id, ProductAvailability.id).all()

    @property
    def reviews(self):
        return object_session(self).query(Review).filter(Review.product_id == self.id).order_by(Review.time_created.desc()).limit(settings.REVIEWS_PER_PAGE).all()


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id], backref=backref(
        "reviews", cascade="all,delete")
    )
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    description = Column(String(
        int(
            env_config.get('VITE_MAX_REVIEW_DESCRIPTION_LENGTH')
        )
    ))
    rating = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    edited = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship(Product, backref=backref(
        "review", cascade="all,delete"))
