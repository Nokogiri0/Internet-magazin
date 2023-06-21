import os

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth import validate_authorized_user
from backend.helpers.images import save_image
from backend.responses import HTTP_401_UNAUTHORIZED
from backend.crud.crud_review import CRUDReview
from backend.crud.crud_user import CRUDUser

from backend.crud.crud_stocks import CRUDStocks

from backend.schemas.product import CreateReview, Review
from backend.schemas.stock import CreateStock, CreateStockForm, Stock
from backend.db.db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/stocks', tags=['Акции'])


@router.post('', response_model=Stock)
def create_stock(
    stock: CreateStockForm,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    StockPicture: UploadFile = File(...)
):
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db, is_admin=True)
    db_image = save_image(upload_file=StockPicture, db=db,
                          user_id=db_user.id)
    crud_stock = CRUDStocks(db)
    db_stock = crud_stock.create_stock(
        name=stock.name,
        open_date=stock.open_date,
        close_date=stock.close_date,
        description=stock.description,
        products=stock.products,
        picture=db_image,
    )
    return db_stock


@router.get('/all')
def get_stocks(page: int = 1, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    if not user_cruds.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_UNAUTHORIZED,
            detail="Нет доступа",
        )
    return CRUDStocks(db).get_stocks(page=page)


@router.get('', response_model=list[Stock])
def get_open_stocks(page: int = 1, db: Session = Depends(get_db)):
    return CRUDStocks(db).get_open_stocks(page=page)


@router.put('/{stock_id}')
def update_stock(
    stock_id: int,
    stock: CreateStockForm,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    StockPicture: UploadFile = File(...)
):
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db, is_admin=True)
    db_image = save_image(upload_file=StockPicture, db=db,
                          user_id=db_user.id)
    crud_stock = CRUDStocks(db)
    db_stock = crud_stock.get_stock_by_id(stock_id=stock_id)
    if not db_stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Акция не найдена")
    db_stock = crud_stock.update_stock(
        db_stock=db_stock,
        name=stock.name,
        open_date=stock.open_date,
        close_date=stock.close_date,
        description=stock.description,
        picture=db_image,
        products=stock.products,
    )
    return db_stock.as_dict()
