from typing import Any
from uuid import UUID
from backend.db.base import CRUDBase
from backend.models.order import Order, OrderProduct, OrderStatus, OrderMessage
from backend.models.stocks import Stock, StockProduct
from backend.schemas.order import CreateOrderProduct as OrderProductSchema
from backend.crud.crud_stocks import CRUDStocks


class CRUDOrder(CRUDBase):
    def get_order(self, id: int) -> Order:
        return self.get(id=id, model=Order)

    def create_order(self, user_id: int, order_items: list[OrderProductSchema], delivery_address_id: int | None,
                     market_id: int | None, stocks: list[Stock]) -> Order:
        order = Order(
            user_id=user_id, delivery_address_id=delivery_address_id, market_id=market_id)
        order = self.create(order)
        order_products = []
        for order_item in order_items:
            db_order_product = self.create(
                OrderProduct(
                    name=order_item.get("product").name,
                    order_id=order.id,
                    product_id=order_item.get("product").id,
                    quantity=order_item.get("quantity"),
                    price=order_item.get("product").price
                )
            )
            order_products.append(db_order_product)
        print(stocks)
        for stock in stocks:
            stock_products = CRUDStocks(self.db).get_stock_products(stock.id)
            stock_product: StockProduct
            print(stock_products)
            for stock_product in stock_products:
                db_order_product = self.create(
                    OrderProduct(
                        name=stock_product.product.name,
                        order_id=order.id,
                        product_id=stock_product.product.id,
                        quantity=stock_product.quantity,
                        price=stock_product.product.price
                    )
                )
                order_products.append(db_order_product)
        order.order_products = order_products
        return self.update(order)

    def change_order_status(self, order: Order, status: OrderStatus) -> Order:
        order.status = status
        return self.update(order)

    def get_orders(self, page: int, page_size=10) -> list[Order]:
        end = page*page_size
        return self.db.query(Order).order_by(Order.time_created.desc()).slice(end-page_size, end).all()

    def get_orders_by_user(self, user_id: int, page: int, page_size=10) -> list[Order]:
        end = page*page_size
        return self.db.query(Order).filter(Order.user_id == user_id).order_by(Order.time_created.desc()).slice(end-page_size, end).all()

    def get_order_messages(self, order_id: int, page, page_size=10) -> list[OrderMessage]:
        end = page*page_size
        return self.db.query(OrderMessage).filter(OrderMessage.order_id == order_id).order_by(OrderMessage.time_created.desc()).slice(end-page_size, end).all()

    def create_order_message(self, order_id: int, user_id: int, message: str) -> OrderMessage:
        return self.create(
            OrderMessage(
                order_id=order_id,
                user_id=user_id,
                message=message
            )
        )

    def get_order_message_by_id(self, id: int) -> OrderMessage:
        return self.get(id=id, model=OrderMessage)

    def update_order_message(self, order_message: OrderMessage, message: str) -> OrderMessage:
        order_message.message = message
        return self.update(order_message)
