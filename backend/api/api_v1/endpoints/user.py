from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth import Authenticate
from backend.helpers.images import save_image

from backend.schemas.user import CreateAddress, UserBase, UserInfo
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import CRUDUser
from backend.db.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.put('/me',  response_model=UserInfo)
def update_user_data(
    UserData: UserBase,
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Обновление данных пользователя'''

    username_user = CRUDUser(Auth.db).get_user_by_username(
        username=UserData.username)

    if username_user and username_user.id != Auth.current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким логином уже существует',
        )
    db_user_updated = CRUDUser(Auth.db).update_user(
        user=Auth.current_user,
        first_name=UserData.first_name,
        last_name=UserData.last_name,
        username=UserData.username,
        phone=UserData.phone,
    )
    return db_user_updated


@router.put('/me/avatar',  response_model=UserInfo)
def update_user_avatar(
    Auth: Authenticate = Depends(Authenticate()),
    userPicture: UploadFile = File(
        default=False, description='Фото пользователя'),
):
    '''Обновление данных пользователя'''
    db_image = save_image(db=Auth.db, upload_file=userPicture,
                          user_id=Auth.current_user.id)
    db_user_updated = CRUDUser(Auth.db).update_user_avatar(
        user=Auth.current_user,
        userPic=db_image,

    )
    return db_user_updated


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")

    return user


@router.post('/addresses', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def create_addresses(AddressData: CreateAddress, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    return user_cruds.create_address(user_id=current_user_id, address=AddressData.address, city=AddressData.city, zip_code=AddressData.zip_code)


@router.get('/addresses/{address_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def get_address(address_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_address = user_cruds.get_address(
        address_id=address_id, user_id=current_user_id)
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Адрес не найден")
    return db_address


@router.put('/addresses/{address_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def update_address(address_id: int, AddressData: CreateAddress, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_address = user_cruds.get_address(
        address_id=address_id, user_id=current_user_id)
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Адрес не найден")
    return user_cruds.update_address(address_id=address_id, address=AddressData.address, city=AddressData.city, zip_code=AddressData.zip_code)


@router.delete('/addresses/{address_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_address = user_cruds.get_address(
        address_id=address_id, user_id=current_user_id)
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Адрес не найден")
    user_cruds.delete_address(db_address=db_address)
