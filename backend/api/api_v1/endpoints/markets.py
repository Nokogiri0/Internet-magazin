from typing import List
from fastapi import Depends, APIRouter, status, HTTPException, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.schemas.market import CreateMarket, MarketInfo
from backend.crud.crud_market import CRUDMarket
from backend.crud.crud_user import CRUDUser
from backend.db.db import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=["Магазины"], prefix="/markets")


@router.get('', response_model=List[MarketInfo])
def get_markets(db: Session = Depends(get_db)):
    market_cruds = CRUDMarket(db)
    markets = market_cruds.get_markets()
    return markets


@router.get('/{market_id}', response_model=MarketInfo)
def get_market(market_id: int, db: Session = Depends(get_db)):
    market_cruds = CRUDMarket(db)
    market = market_cruds.get_market_by_id(market_id)
    if not market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Магазин не найден")
    return market


@router.post('', status_code=status.HTTP_201_CREATED)
def create_market(
        marketData: CreateMarket,
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not CRUDUser(db).is_admin(current_user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет доступа")
    market_cruds = CRUDMarket(db)
    return market_cruds.create_market(
        address=marketData.address,
        description=marketData.description,
        phone=marketData.phone,
        weekday_hours=marketData.weekday_hours,
        weekend_hours=marketData.weekend_hours,
    )


@router.put('/{market_id}', status_code=status.HTTP_200_OK)
def update_market(
    market_id: int,
    marketData: CreateMarket,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not CRUDUser(db).is_admin(current_user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет доступа")
    market_cruds = CRUDMarket(db)
    db_market = market_cruds.get_market_by_id(market_id)
    if not db_market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Магазин не найден")
    return market_cruds.update_market(
        db_market=db_market,
        address=marketData.address,
        description=marketData.description,
        phone=marketData.phone,
        weekday_hours=marketData.weekday_hours,
        weekend_hours=marketData.weekend_hours,
    )


@router.delete('/{market_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_market(
    market_id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not CRUDUser(db).is_admin(current_user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет доступа")
    market_cruds = CRUDMarket(db)
    db_market = market_cruds.get_market_by_id(market_id)
    if not db_market:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Магазин не найден")
    return market_cruds.delete_market(db_market=db_market)
