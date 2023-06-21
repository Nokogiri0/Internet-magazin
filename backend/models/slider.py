from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.core.config import env_config


class Slide(Base):
    __tablename__ = 'slides'
    id = Column(Integer, primary_key=True)
    name = Column(String(
        int(env_config.get('VITE_MAX_SLIDE_NAME_LENGTH'))
    ), index=True)
    open_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime)
    url = Column(String(
        int(env_config.get('VITE_MAX_SLIDE_URL_LENGTH'))))
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
            name='products_picture_id_fkey',
        )
    )
    picture = relationship("Image", foreign_keys=[
        picture_id], cascade="all,delete")
    position = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
