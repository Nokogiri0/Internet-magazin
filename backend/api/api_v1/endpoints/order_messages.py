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


router = APIRouter(tags=["Чат заказов"], prefix="/order-messages")


@router.put("/{message_id}", response_model=OrderMessage)
def update_order_message(message_id: UUID, message_data: CreateOrderMessage, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required()
    db_user = validate_authorized_user(authorize, db)
    db_message = CRUDOrder(db).get_order_message_by_id(message_id)
    if not db_message:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND,
                            detail="Сообщение не найдено")
    if db_message.user_id != db_user.id:
        raise HTTPException(status_code=fastapi_status.HTTP_403_FORBIDDEN,
                            detail="Нет доступа")
    return CRUDOrder(db).update_order_message(order_message=db_message, message=message_data.message)
