from fastapi import APIRouter, HTTPException, status
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_review import CRUDReview
from backend.crud.crud_user import CRUDUser
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.schemas.product import CreateReview, Review

router = APIRouter(prefix='/reviews', tags=['Отзывы'])


@router.get('/my', response_model=list[Review])
def get_my_reviews(page: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    crud_review = CRUDReview(db)
    db_reviews = crud_review.get_reviews_by_user_id(
        user_id=current_user_id, page=page)
    return [review.as_dict() for review in db_reviews]


@router.get('/{review_id}', response_model=Review)
def get_review(review_id: int, db: Session = Depends(get_db)):
    crud_review = CRUDReview(db)
    db_review = crud_review.get_review_by_id(review_id=review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Отзыв не найден")
    return db_review.as_dict()


@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    crud_review = CRUDReview(db)
    db_review = crud_review.get_review_by_id(review_id=review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Отзыв не найден")
    user_cruds = CRUDUser(db)
    db_user = user_cruds.get_user_by_id(user_id=current_user_id)
    if not db_user or db_review.user_id != current_user_id and not db_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_review.delete_review(review=db_review)


@router.put('/{review_id}', response_model=Review)
def edit_review(review_id: int, review_data: CreateReview, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    crud_review = CRUDReview(db)
    db_review = crud_review.get_review_by_id(review_id=review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Отзыв не найден")
    if db_review.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    db_review = crud_review.edit_review(
        review=db_review, description=review_data.description, rating=review_data.rating)
    return db_review
