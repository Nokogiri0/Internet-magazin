from backend.db.session import SessionLocal
import logging
from backend.schemas.user import UserWithTypeRegister
from backend.crud.crud_user import CRUDUser
logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin"


def init_db() -> None:  # 1
    logger.info("Инициализация базы данных")
    if FIRST_SUPERUSER:
        user_cruds = CRUDUser(SessionLocal())
        user = user_cruds.get_user_by_username(FIRST_SUPERUSER)  # 2
        if not user:
            user_in = UserWithTypeRegister(
                username=FIRST_SUPERUSER,
                first_name=FIRST_SUPERUSER,
                password='abobus123',
                type='superuser'
            )
            user_cruds.create_user(user_in, admin=True)
            logger.info(f"Администратор {FIRST_SUPERUSER} создан")
        else:
            logger.warning(
                "Пропуск создания аккаунта администратора. Пользователь с юзернеймом "
                f"{FIRST_SUPERUSER} уже существует"
            )
    logger.info("Инициализация базы данных закончена")
