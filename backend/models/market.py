from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String
from backend.core.config import env_config


class Market(Base):
    __tablename__ = 'markets'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(
        int(env_config.get("VITE_MAX_ADDRESS_LENGTH"))
    ), nullable=False)
    description = Column(String(
        int(env_config.get("VITE_MAX_MARKET_DESCRIPTION_LENGTH"))
    ))
    weekday_hours = Column(String, nullable=False)
    weekend_hours = Column(String, nullable=False)
    phone = Column(String, nullable=False)
