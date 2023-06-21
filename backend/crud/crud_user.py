from backend.db.base import CRUDBase
from backend.schemas.user import UserAuth, UserModifiable, UserRegister
from backend.models.user import User, UserAddress
from backend.models.files import Image
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from backend.crud.crud_file import CRUDFile
from fastapi import HTTPException


class CRUDUser(CRUDBase):

    def __init__(self, db) -> None:
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def update_user_avatar(self, user: User,  userPic: Image) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        if userPic and user.picture:
            CRUDFile(self.db).replace_old_picture(
                model=user, new_picture=userPic)
        elif userPic:
            user.picture = userPic
        elif user.picture:
            self.delete(user.picture)

        return self.update(user)

    def create_user(self, user: UserRegister, admin=False) -> User:
        password_hash = self.pwd_context.hash(user.password)
        user_in_data = jsonable_encoder(user)
        del user_in_data['password']
        db_user = User(hashed_password=password_hash,
                       **user_in_data)
        if admin:
            db_user.is_superuser = True
        else:
            db_user.is_superuser = False
        return self.create(db_user)

    def login(self, user: UserAuth) -> User | None:
        db_user = self.get_user_by_username(username=user.username)
        if not db_user:
            return None
        if not self.pwd_context.verify(user.password, db_user.hashed_password):
            return None
        return db_user

    def update_user(self, user: User, first_name: str | None, last_name: str | None, username: str | None, phone: str | None) -> User:
        if user is None:
            raise Exception('Update user failed: user is None')
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.username = username
        return self.create(user)

    def is_admin(self, user_id):
        db_user = self.get_user_by_id(user_id=user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.is_superuser:
            return db_user

    def create_address(self, user_id: int, city: str,  address: str, zip_code: int) -> UserAddress:
        return self.create(UserAddress(user_id=user_id, city=city,  address=address, zip_code=zip_code))

    def get_address(self, user_id: int, address_id: int) -> UserAddress:
        return self.db.query(UserAddress).filter(UserAddress.user_id == user_id, UserAddress.id == address_id).first()

    def update_address(self, db_address: UserAddress, city: str, address: str, zip_code: int) -> UserAddress:
        db_address.city = city
        db_address.address = address
        db_address.zip_code = zip_code
        return self.update(db_address)

    def delete_address(self, db_address: UserAddress):
        self.delete(db_address)
