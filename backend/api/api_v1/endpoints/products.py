import os

from fastapi import APIRouter, HTTPException, status
from typing import List
from fastapi import Depends, APIRouter, status, HTTPException, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_catalog import CRUDCatalog
from backend.crud.crud_review import CRUDReview

from backend.helpers.auth import Authenticate
from backend.helpers.images import save_image
from backend.helpers.products import get_product_json
from backend.schemas.product import CreateProductAvailability, CreateProductForm, Product, ProductAvailability, ProductAvailabilityMarket, UpdateProduct
from backend.responses import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import CRUDUser
from backend.crud.crud_products import CRUDProduct
from backend.schemas.product import CreateReview, Review

from backend.db.db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix='/products', tags=['Товары'])


@router.put('/{product_id}',
            responses={**HTTP_401_UNAUTHORIZED},
            response_model=Product,
            )
def update_product(product_id: int, product_data: UpdateProduct,  ProductPicture: UploadFile = File(default=False),
                   Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    admin = CRUDUser(db).is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_product = CRUDProduct(db)
    db_product = crud_product.get_product_by_id(
        product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=db_product.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    db_image_min, db_image = save_image(upload_file=ProductPicture, db=db,
                                        user_id=current_user_id,  with_big=True)
    db_product = crud_product.update_product(
        db_product=db_product,
        name=product_data.name,
        price=product_data.price,
        description=product_data.description,
        picture=db_image,
        picture_min=db_image_min,
        characteristics=product_data.characteristics
    )
    return db_product


@router.get('/{product_id}',
            responses={**HTTP_401_UNAUTHORIZED},
            response_model=Product
            )
def get_product(product_id: int, Auth: Authenticate = Depends(Authenticate(required=False))):
    '''Получение товара'''
    db_product = CRUDProduct(Auth.db).get_product_by_id(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    return db_product


@router.get('/{product_id}/availability', response_model=ProductAvailability)
def get_product_available(product_id: int, db: Session = Depends(get_db)):
    '''Наличие товара'''
    db_product = CRUDProduct(db).get_product_by_id(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    product_cruds = CRUDProduct(db)
    return product_cruds.get_product_availability(product_id=product_id)


@router.put(
    '/{product_id}/availability',
    responses={**HTTP_401_UNAUTHORIZED},
    response_model=CreateProductAvailability
)
def update_product_available(product_id: int,
                             product_data: CreateProductAvailability,
                             Authorize: AuthJWT = Depends(),
                             db: Session = Depends(get_db)):
    '''Добавление наличия товара'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    admin = user_cruds.is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    db_product = CRUDProduct(db).get_product_by_id(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    product_cruds = CRUDProduct(db)
    db_product_availability = product_cruds.update_product_availability(
        product_id=product_id,
        market_id=product_data.market_id,
        quantity=product_data.quantity
    )
    return CreateProductAvailability(
        market_id=db_product_availability.market_id,
        quantity=db_product_availability.quantity,
        product_id=db_product_availability.product_id,
    )


@router.put('/{product_id}/move',
            responses={**HTTP_401_UNAUTHORIZED},
            response_model=Product,
            )
def move_product(product_id: int, category_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    admin = user_cruds.is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    db_product = user_cruds.get_product_by_id(
        product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    category = CRUDCatalog(db).get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    crud_product = CRUDProduct(db)
    return get_product_json(crud_product.change_category(db_product=db_product, category_id=category_id))


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    admin = CRUDUser(db).is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    current_user_id = Authorize.get_jwt_subject()
    crud_product = CRUDProduct(db)
    db_product = crud_product.get_product_by_id(
        product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_product.delete_product(product=db_product)


@router.get('/{product_id}/reviews', response_model=List[Review])
def get_product_reviews(product_id: int, page: int = 1, db: Session = Depends(get_db)):
    '''Получение отзывов о товаре'''
    crud_product = CRUDProduct(db)
    db_product = crud_product.get_product_by_id(product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_review = CRUDReview(db)
    db_reviews = crud_review.get_last_product_reviews(
        product_id=product_id, page=page)
    return [db_review.as_dict() for db_review in db_reviews]


@router.post('/{product_id}/reviews',
             responses={**HTTP_401_UNAUTHORIZED},
             response_model=Review,
             )
def create_review(product_id: int, review_data: CreateReview, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    crud_product = CRUDProduct(db)
    db_product = crud_product.get_product_by_id(
        product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Товар не найден")
    crud_review = CRUDReview(db)
    is_has_review = crud_review.has_review(
        product_id=product_id, user_id=current_user_id)
    if is_has_review:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Вы уже оставили отзыв")

    db_review = crud_review.create_review(
        product_id=product_id,
        user_id=current_user_id,
        description=review_data.description,
        rating=review_data.rating
    )
    return db_review.as_dict()
