from typing import Any
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.products import Product, Category
from backend.crud.crud_products import CRUDProduct
from backend.core.config import settings, env_config
from backend.models.order import OrderProduct, Order, OrderStatus
from sqlalchemy import func


class CRUDCatalog(CRUDBase):

    def get(self, model, id: int) -> Any | None:
        return self.db.query(model).filter(model.id == id).first()

    def create_category(self, *, name: str, parent_id: int | None, db_image: Image) -> Category:
        return self.create(Category(name=name, parent_id=parent_id, picture=db_image))

    def update_category(self, category: Category, name: str):
        category.name = name
        return self.create(category)

    def detele_category(self, category_id: int):
        node = self.db.query(Category).filter(Category.id == category_id).one()
        self.delete(node)

    def get_category(self, category_id: int) -> Category:
        return self.get(model=Category, id=category_id)

    def category_has_products(self, category_id: int):
        return bool(self.db.query(Product).filter(Product.category_id == category_id).first())

    def get_categories(self, category: Category):
        return category.get_tree(self.db, json=True)

    def get_products_category(self, category_id: int, order_by: settings.ProductSort, page: int, order: settings.Order, page_size=int(env_config.get('VITE_PRODUCTS_PER_PAGE'))):
        end = page * page_size
        start = end - page_size
        query = self.db.query(Product)
        if order_by == settings.ProductSort.popularity:
            subquery = self.db.query(OrderProduct.product_id, func.count(OrderProduct.product_id).label('count')).join(
                Order).filter(Order.status == OrderStatus.done).group_by(OrderProduct.product_id).subquery()
            query = query.outerjoin(
                subquery, Product.id == subquery.c.product_id)
            # Use Product.id as a fallback if count is None
            order_column = subquery.c.count if subquery.c.count is not None else Product.id
        else:
            order_column = getattr(Product, order_by.value)
        if order_by == settings.ProductSort.price:
            order = settings.Order.asc if order == settings.Order.desc else settings.Order.desc
        if order == settings.Order.asc:
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        return query.filter(Product.category_id == category_id).slice(start, end).all()

    # поломався сортировка по популярности

    def get_root_categories(self):
        return self.db.query(Category).filter(Category.parent_id == None).all()

    def update_category(self, category: Category, name: str):
        category.name = name
        return self.create(category)

    def has_content(self, category_id: int):
        has_products = bool(self.db.query(Product).filter(
            Product.category_id == category_id).first())
        has_children = bool(self.db.query(Category).filter(
            Category.parent_id == category_id).first())
        return has_products or has_children

    def move_products(self, category_id: int, new_category_id: int):
        products = self.db.query(Product).filter(
            Product.category_id == category_id).all()
        for product in products:
            product.category_id = new_category_id
            self.create(product)
