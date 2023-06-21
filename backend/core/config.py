from enum import Enum
from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Literal, Optional, Tuple, get_args
from dotenv import dotenv_values
import os


env_config = {**dotenv_values('.env'), **
              dotenv_values(".env.local"), **os.environ}


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = ''
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:4000', 'http://192.168.50.106:4000']
    DATABASE_URI: Optional[str] = f"postgresql://{env_config['DB_USER']}:{env_config['DB_PASSWORD']}@{env_config['DB_HOST']}:{env_config['DB_PORT']}/{env_config['DB_NAME']}"
    TEST_DATABASE_URI: Optional[str] = f"{DATABASE_URI}_test"
    FIRST_SUPERUSER: str = "admin"
    ASSETS_FOLDER: str = 'assets/'
    IMAGES_FOLDER: str = ASSETS_FOLDER+'images'
    OTHER_FILES_FOLDER: str = ASSETS_FOLDER+'other'
    IMAGES_EXTENTION: str = '.png'
    UPLOADS_ROUTE: str = '/uploads'
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"
    REVIEWS_PER_PAGE: int = 10

    TEST_USER_USERNAME = 'test_user'
    TEST_ADMIN_USERNAME = 'admin'

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False

    class ProductSort(Enum):
        name = 'name'
        popularity = 'popularity'
        price = 'price'

    class Order(Enum):
        asc = 'asc'
        desc = 'desc'


settings = Settings()
