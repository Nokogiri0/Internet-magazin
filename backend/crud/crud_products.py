from backend.crud.crud_file import CRUDFile
from backend.db.base import CRUDBase
from backend.models.market import Market
from backend.models.products import Product
from backend.models.availability import ProductAvailability
from backend.schemas.product import ProductAvailability as ProductAvailabilitySchema, ProductAvailabilityMarket
from backend.models.files import Image
from backend.crud.crud_market import CRUDMarket


class CRUDProduct(CRUDBase):
    def delete_product(self, product: Product):
        self.delete(product)

    def create_product(self, name: str, category_id: int, characteristics: dict, price: int, pic: Image, pic_min: Image, description: str | None) -> Product:
        db_product = Product(
            name=name,
            category_id=category_id,
            characteristics=characteristics,
            price=price, description=description,
            picture=pic_min,
            picture_min=pic
        )
        return self.create(db_product)

    def get_product_by_id(self, product_id: int) -> Product:
        return self.get(model=Product, id=product_id)

    def update_product(self, db_product: Product, name: str, price: int, description: str, picture: Image, picture_min: Image,  characteristics: dict):
        db_product.price = price
        db_product.name = name
        db_product.description = description
        if picture:
            CRUDFile(self.db).replace_old_picture(
                model=db_product, new_picture=picture)
            CRUDFile(self.db).replace_old_picture(
                model=db_product, new_picture=picture_min, key='picture_min')
        db_product.characteristics = characteristics
        return self.update(db_product)

    def change_category(self, db_product: Product, category_id: int):
        db_product.category_id = category_id
        return self.update(db_product)

    def delete_product(self, product: Product):
        self.delete(product)

    def get_product_available_in_market(self, product_id: int, market_id: int) -> ProductAvailability:
        return self.db.query(ProductAvailability).filter(ProductAvailability.product_id == product_id, ProductAvailability.market_id == market_id).first()

    def get_product_availability(self, product_id: int) -> ProductAvailabilitySchema:
        availability = self.db.query(ProductAvailability).filter(
            ProductAvailability.product_id == product_id).all()
        available_markets_ids = [store.market_id for store in availability]
        markets = CRUDMarket(self.db).get_markets()
        availability_in_markets = []
        available_market: ProductAvailability
        for available_market in availability:
            availability_in_markets.append(
                ProductAvailabilityMarket(
                    id=available_market.market_id,
                    description=available_market.market.description,
                    address=available_market.market.address,
                    weekday_hours=available_market.market.weekday_hours,
                    weekend_hours=available_market.market.weekend_hours,
                    phone=available_market.market.phone,
                    quantity=available_market.quantity,
                )
            )
            if available_market.market_id in available_markets_ids:
                markets.remove(available_market.market)
        for market in markets:
            availability_in_markets.append(
                ProductAvailabilityMarket(
                    id=market.id,
                    description=market.description,
                    address=market.address,
                    weekday_hours=market.weekday_hours,
                    weekend_hours=market.weekend_hours,
                    phone=market.phone,
                    quantity=0,
                )
            )
        availability_in_markets.sort(key=lambda x: x.quantity, reverse=True)
        return ProductAvailabilitySchema(
            product_id=product_id,
            markets=availability_in_markets
        )

    def update_product_availability(self, product_id: int, market_id: int, quantity: int) -> ProductAvailability:
        availability = self.get_product_available_in_market(
            product_id=product_id, market_id=market_id)
        if availability:
            availability.quantity = quantity
            return self.update(availability)
        else:
            availability = ProductAvailability(
                product_id=product_id,
                market_id=market_id,
                quantity=quantity
            )
            return self.create(availability)
