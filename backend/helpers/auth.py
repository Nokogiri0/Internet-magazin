from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.config import settings
from backend.crud.crud_user import CRUDUser
from backend.db.db import get_db
from fastapi import Depends


def validate_authorized_user(Authorize: AuthJWT, db: Session, is_admin=False) -> User:
    current_user_id = Authorize.get_jwt_subject()
    db_user = CRUDUser(db).get_user_by_id(user_id=current_user_id)
    if not db_user:
        raise HTTPException(
            status_code=403,
            detail="Авторизованный пользователь не найден"
        )
    if is_admin and not db_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="У вас недостаточно прав для выполнения данного действия"
        )
    return db_user


class Authenticate:
    def __init__(
        self,
        is_admin: bool = False,
        required: bool = True,
    ):
        self.is_admin = is_admin
        self.required = required
        self.db = None
        self.current_user_id = None
        self.Authorize = None

    def __call__(self, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
        self.db = db
        self.current_user = None

        if self.required:
            try:
                Authorize.jwt_required()
                current_user_id = Authorize.get_jwt_subject()
            except:
                if self.required:
                    raise HTTPException(
                        status_code=403,
                        detail="Необходима авторизация"
                    )
                else:
                    return self
        else:
            try:
                Authorize.jwt_optional()
                current_user_id = Authorize.get_jwt_subject()
            except:
                current_user_id = None

        if not current_user_id and not self.required:
            return self
        db_user = CRUDUser(db).get_user_by_id(user_id=current_user_id)
        if not db_user:
            if self.required:
                raise HTTPException(
                    status_code=403,
                    detail="Авторизованный пользователь не найден"
                )
            else:
                Authorize.unset_jwt_cookies()
                return self
        if self.is_admin and not db_user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail=f"У вас недостаточно прав для выполнения этого действия, требуемый тип пользователя: Администратор",
            )
        self.current_user = db_user
        self.current_user_id = current_user_id
        return self
