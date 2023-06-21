from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter, status as fastapi_status, HTTPException, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_market import CRUDMarket
from backend.crud.crud_order import CRUDOrder
from backend.crud.crud_stocks import CRUDStocks
from backend.crud.crud_products import CRUDProduct
from backend.helpers.auth import validate_authorized_user
from backend.models.order import OrderStatus
from backend.schemas.order import CreateOrder, CreateOrderMessage, Order, OrderMessage
from backend.responses import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import CRUDUser
from backend.db.db import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("", response_model=List[Order])
def get_orders(page: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    if not db_user.is_superuser:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    orders = CRUDOrder(db).get_orders(page=page)
    return orders


@router.post("", response_model=Order)
def create_order(orderData: CreateOrder, authorize: AuthJWT = Depends(), db: Session = Depends(get_db),):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    if len(list(filter(lambda x: x is None, [orderData.market_id, orderData.delivery_address_id]))) != 1:
        raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                            detail="укажите адрес доставки или магазин")
    if orderData.market_id is not None:
        market = CRUDMarket(db).get_market_by_id(orderData.market_id)
        if not market:
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                                detail="Магазин не найден")
    if orderData.delivery_address_id is not None:
        if not CRUDUser(db).get_address(user_id=db_user.id, address_id=orderData.delivery_address_id):
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                                detail="Адрес не найден")
    crud_product = CRUDProduct(db)
    products = []
    for order_product in orderData.products:
        db_product = crud_product.get_product_by_id(order_product.product_id)
        if not db_product:
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                                detail="товар не найден")
        products.append({"product": db_product,
                        "quantity": order_product.quantity})
    stocks = []
    crud_stock = CRUDStocks(db)
    for stock_id in orderData.stocks:
        db_stock = crud_stock.get_stock_by_id(stock_id=stock_id)
        if not db_stock:
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                                detail="акция не найдена")
        stocks.append(db_stock)
    order = CRUDOrder(db).create_order(
        user_id=db_user.id,
        order_items=products,
        delivery_address_id=orderData.delivery_address_id,
        market_id=orderData.market_id,
        stocks=stocks)
    return order


@router.put("/{order_id}/status", response_model=Order)
def change_order_status(order_id: UUID, status: OrderStatus, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    order = CRUDOrder(db).get_order(order_id)
    if not order:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                            detail="Заказ не найден")
    if order.user_id != db_user.id and not db_user.is_superuser:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    if not db_user.is_superuser and status != OrderStatus.cancelled:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    order = CRUDOrder(db).change_order_status(order=order, status=status)
    return order


@router.get("/my", response_model=List[Order])
def get_my_orders(page: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    orders = CRUDOrder(db).get_orders_by_user(page=page, user_id=db_user.id)
    return orders


@router.get("/{order_id}", response_model=Order)
def get_order(order_id: UUID, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    order = CRUDOrder(db).get_order(order_id)
    if not order:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                            detail="Заказ не найден")
    if order.user_id != db_user.id and not db_user.is_superuser:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    return order


@router.get("/{order_id}/messages", response_model=List[OrderMessage])
def get_order_messages(order_id: UUID, page: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    order = CRUDOrder(db).get_order(order_id)
    if not order:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                            detail="Заказ не найден")
    if order.user_id != db_user.id and not db_user.is_superuser:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    messages = CRUDOrder(db).get_order_messages(order_id=order_id, page=page)
    return messages


@router.post("/{order_id}/messages", response_model=OrderMessage)
def create_order_message(order_id: UUID, message_data: CreateOrderMessage, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    order = CRUDOrder(db).get_order(order_id)
    if not order:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                            detail="Заказ не найден")
    if order.user_id != db_user.id and not db_user.is_superuser:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Недостаточно прав")
    message = CRUDOrder(db).create_order_message(
        order_id=order_id, message=message_data.message, user_id=db_user.id)
    return message
