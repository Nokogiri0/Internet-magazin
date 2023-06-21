from backend.models.user import *
from backend.models.files import *
from backend.models.slider import *
from backend.models.availability import *
from backend.models.cart import *
from backend.models.market import *
from backend.models.order import *
from backend.models.products import *
from backend.models.stocks import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from backend.db.base_class import Base
from backend.core.config import settings


engine = create_engine(
    settings.DATABASE_URI,
)

if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
