from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from backend.core.config import env_config


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(
        String(int(env_config.get('VITE_MAX_FIRSTNAME_LENGTH'))), nullable=True)
    last_name = Column(
        String(int(env_config.get('VITE_MAX_LASTNAME_LENGTH'))), nullable=True)
    username = Column(String(
        int(env_config.get('VITE_MAX_LASTNAME_LENGTH'))), index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "images.id",
            name='users_picture_id_fkey',
            ondelete='SET NULL'
        )
    )
    picture = relationship("Image", foreign_keys=[
                           picture_id], cascade="all,delete")
    phone = Column(String)


class UserAddress(Base):
    __tablename__ = 'user_addresses'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship(User, backref=backref(
        "addresses", cascade="all,delete"), foreign_keys=[user_id])
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
