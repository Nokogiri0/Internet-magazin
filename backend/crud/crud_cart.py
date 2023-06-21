from typing import Any, List
from backend.db.base import CRUDBase
from backend.models.cart import CartProduct, CartStock


class CRUDCart(CRUDBase):

    def get_cart_products(self, user_id: int) -> List[CartProduct]:
        return self.db.query(CartProduct).filter(CartProduct.user_id == user_id).all()

    def get_cart_stocks(self, user_id: int) -> List[CartStock]:
        return self.db.query(CartStock).filter(CartStock.user_id == user_id).all()

    def get_cart_product(self, user_id: int, product_id: int) -> CartProduct | None:
        return self.db.query(CartProduct).filter(CartProduct.user_id == user_id, CartProduct.product_id == product_id).first()

    def get_cart_product_by_id(self, cart_product_id: int) -> CartProduct | None:
        return self.db.query(CartProduct).filter(CartProduct.cart_product_id == cart_product_id).first()

    def clear_cart(self, user_id: int):
        self.db.query(CartProduct).filter(
            CartProduct.user_id == user_id).delete()
        self.db.query(CartStock).filter(CartStock.user_id == user_id).delete()
        self.db.commit()

    def get_cart_stock(self, user_id: int, stock_id: int) -> CartStock | None:
        return self.db.query(CartStock).filter(CartStock.user_id == user_id, CartStock.stock_id == stock_id).first()

    def get_cart_stock_by_id(self, cart_stock_id: int) -> CartStock | None:
        return self.db.query(CartStock).filter(CartStock.cart_stock_id == cart_stock_id).first()

    def change_product_quantity(self, cart_product: CartProduct, quantity: int):
        cart_product.quantity = quantity
        return self.update(cart_product)

    def change_stock_quantity(self, cart_stock: CartStock, quantity: int):
        cart_stock.quantity = quantity
        return self.update(cart_stock)

    def add_product_to_cart(self, product_id: int, quantity: int, user_id: int):
        cart_product = self.get_cart_product(user_id, product_id)
        if cart_product:
            cart_product.quantity += quantity
            cart_product = self.update(cart_product)
        else:
            cart_product = self.create(CartProduct(
                product_id=product_id, quantity=quantity, user_id=user_id))
        return cart_product

    def add_stock_to_cart(self, stock_id: int, quantity: int, user_id: int):
        cart_stock = self.get_cart_stock(user_id, stock_id)
        if cart_stock:
            cart_stock.quantity += quantity
            cart_stock = self.update(cart_stock)
        else:
            cart_stock = self.create(CartStock(
                stock_id=stock_id, quantity=quantity, user_id=user_id))
        return cart_stock

    def delete_product_from_cart(self, user_id: int, product_id: int):
        cart_product = self.get_cart_product(user_id, product_id)
        if cart_product:
            self.delete(cart_product)

    def delete_stock_from_cart(self, user_id: int, stock_id: int):
        cart_stock = self.get_cart_stock(user_id, stock_id)
        if cart_stock:
            self.delete(cart_stock)
