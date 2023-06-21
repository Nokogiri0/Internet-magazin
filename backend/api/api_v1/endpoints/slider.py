from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi import Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.helpers.auth import validate_authorized_user
from backend.core.config import env_config, settings
from backend.crud.crud_slider import CRUDSlider
from backend.helpers.images import save_image

from backend.schemas.slider import CreateSlide, CreateSlideForm, Slide

router = APIRouter(prefix='/slider', tags=['Слайдер'])


@router.post('', response_model=Slide, status_code=status.HTTP_201_CREATED)
def create_slide(
    slide: CreateSlideForm = Depends(CreateSlideForm),
    SlidePicture: UploadFile = File(...),
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db, is_admin=True)
    db_image = save_image(upload_file=SlidePicture, db=db,
                          user_id=db_user.id, resize_image_options=(3000, 3000))
    db_slide = CRUDSlider(db).create_slide(
        name=slide.name,
        open_date=slide.open_date,
        close_date=slide.close_date,
        url=slide.url,
        picture=db_image,
        position=slide.position,
        is_active=slide.is_active
    )
    return db_slide


# @router.put('/{slide_id}', response_model=Slide)
# def update_slide(
#     slide_id: int,
#     slide: CreateSlide = Depends(CreateSlide),
#     SlidePicture: UploadFile = File(default=False),
#     db: Session = Depends(get_db),
#     Authorize: AuthJWT = Depends()
# ):
#     Authorize.jwt_required()
#     db_user = validate_authorized_user(Authorize, db, is_admin=True)
#     db_slide = CRUDSlider(db).get_slide_by_id(slide_id=slide_id)
#     if not db_slide:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Слайд не найден'
#         )
#     db_image = save_image(upload_file=SlidePicture, db=db,
#                           user_id=db_user.id, resize_image_options=(3000, 3000))
#     db_slide = CRUDSlider(db).update_slide(
#         slide=db_slide,
#         name=slide.name,
#         open_date=slide.open_date,
#         close_date=slide.close_date,
#         url=slide.url,
#         picture=db_image,
#         position=slide.position,
#         is_active=slide.is_active
#     )
#     return db_slide


@router.get('/{slide_id}', response_model=Slide)
def get_slide_by_id(
    slide_id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    validate_authorized_user(Authorize, db, is_admin=True)
    db_slide = CRUDSlider(db).get_slide_by_id(slide_id=slide_id)
    if not db_slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Слайд не найден'
        )
    return db_slide


@router.delete('/{slide_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_slide_by_id(
    slide_id: int,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    validate_authorized_user(Authorize, db, is_admin=True)
    db_slide = CRUDSlider(db).get_slide_by_id(slide_id=slide_id)
    if not db_slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Слайд не найден'
        )
    CRUDSlider(db).delete_slide_by_id(slide=db_slide)


@router.get('', response_model=list[Slide])
def get_all_slides(
    db: Session = Depends(get_db),
):
    db_slides = CRUDSlider(db).get_active_slides()
    return db_slides
