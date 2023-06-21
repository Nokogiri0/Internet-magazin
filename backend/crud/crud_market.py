from backend.db.base import CRUDBase
from backend.models.market import Market


class CRUDMarket(CRUDBase):
    def get_markets(self) -> Market:
        return self.db.query(Market).all()

    def get_market_by_id(self, market_id: int) -> Market:
        return self.get(id=market_id, model=Market)

    def create_market(self, *, address: str, description: str, weekday_hours: str, weekend_hours: str, phone: str) -> Market:
        db_market = Market(
            address=address,
            description=description,
            weekday_hours=weekday_hours,
            weekend_hours=weekend_hours,
            phone=phone
        )
        return self.create(db_market)

    def update_market(self, *, db_market: Market, address: str, description: str, weekday_hours: str, weekend_hours: str, phone: str) -> Market:
        db_market.address = address
        db_market.description = description
        db_market.weekday_hours = weekday_hours
        db_market.weekend_hours = weekend_hours
        db_market.phone = phone
        return self.update(db_market)

    def delete_market(self, *, db_market) -> Market:
        return self.delete(model=db_market)
