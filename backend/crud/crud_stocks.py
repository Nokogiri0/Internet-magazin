from datetime import datetime
from typing import List
from backend.core.config import settings
from backend.crud.crud_file import CRUDFile
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.stocks import Stock, StockProduct
from backend.schemas.stock import StockProduct as StockProductSchema
from sqlalchemy import case, or_


class CRUDStocks(CRUDBase):
    def create_stock(self, *, name: str, open_date: datetime, close_date: datetime, description: str, products: List[StockProductSchema], picture: Image) -> Stock:
        db_stock = self.create(Stock(name=name, open_date=open_date,
                                     close_date=close_date, description=description, picture=picture))
        stock_products = []
        for product in products:
            db_stock_product = self.create(
                StockProduct(
                    stock_id=db_stock.id,
                    product_id=product.product_id,
                    quantity=product.quantity,
                    price=product.price
                )
            )
            stock_products.append(db_stock_product)
        db_stock.products = stock_products
        return self.update(db_stock)

    def get_stocks(self, *, page: int) -> Stock:
        return self.get_multi(Stock, page=page)

    def get_open_stocks(self, page: int) -> Stock:
        page_size: int = settings.REVIEWS_PER_PAGE
        end = page * page_size
        now = datetime.now().strftime('%Y-%m-%d')
        return self.db.query(Stock)\
            .filter(Stock.open_date <= now, or_(Stock.close_date.is_(None), Stock.close_date >= now))\
            .order_by(Stock.open_date.desc())\
            .all()
        # return self.db.query(Stock).filter(Stock.open_date >= now).filter(Stock.close_date <= now).filter(
        #     case([
        #         (Stock.close_date != None, Stock.close_date <= now),
        #     ], else_=True)).slice(end-page_size, end).all()

    def update_stock(self, *, db_stock: Stock, name: str, open_date: datetime, close_date: datetime, description: str, picture: Image, products: List[StockProductSchema]) -> Stock:
        db_stock.name = name
        db_stock.open_date = open_date
        db_stock.close_date = close_date
        db_stock.description = description
        if picture:
            CRUDFile(self.db).replace_old_picture(
                model=db_stock, new_picture=picture)

        for product in products:
            db_stock_product = self.db.query(StockProduct).filter(
                StockProduct.stock_id == db_stock.id, StockProduct.product_id == product.product_id).first()
            if db_stock_product:
                db_stock_product.quantity = product.quantity
                db_stock_product.price = product.price
                self.update(db_stock_product)
            else:
                db_stock_product = self.create(
                    StockProduct(
                        stock_id=db_stock.id,
                        product_id=product.product_id,
                        quantity=product.quantity,
                        price=product.price
                    )
                )

        return self.update(db_stock)

    def get_stock_by_id(self, *, stock_id: int) -> Stock:
        return self.get(id=stock_id, model=Stock)

    def get_stock_products(self, stock_id: int) -> StockProduct:
        return self.db.query(StockProduct).filter(StockProduct.stock_id == stock_id).all()
