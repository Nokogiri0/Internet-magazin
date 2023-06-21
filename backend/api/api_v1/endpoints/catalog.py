from typing import List
from fastapi import Depends, APIRouter, File, UploadFile, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.crud.crud_catalog import CRUDCatalog
from backend.crud.crud_products import CRUDProduct
from backend.helpers.auth import validate_authorized_user
from backend.helpers.category import set_category_info, set_category_info_no_products, set_new_category_info
from backend.helpers.images import save_image

from backend.helpers.products import get_product_json
from backend.schemas.catalog import CategoryInfo, CreateCategory,  Categories, CreateCategoryBase, CreateCategoryForm, CreatedCategory
from backend.schemas.product import CatalogProduct, CreateProductForm, Product, UpdateProductModel
from backend.models.products import Category as CategoryModel
from backend.responses import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import CRUDUser
from fastapi.encoders import jsonable_encoder
from backend.db.db import get_db
from sqlalchemy.orm import Session

categories_router = APIRouter(tags=["Categories"], prefix="/categories")


@categories_router.post('',
                        responses={**HTTP_401_UNAUTHORIZED},
                        response_model=CreatedCategory, status_code=status.HTTP_201_CREATED)
def create_category(categoryData: CreateCategoryForm,
                    CategoryPicture: UploadFile = File(...),
                    Authorize: AuthJWT = Depends(),
                    db: Session = Depends(get_db)):
    '''
    Создает категорию в каталоге если parent_id не задан или None, а если задан создает подкатегорию заданной категории или подкатегории
    '''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db, is_admin=True)
    catalog_crud = CRUDCatalog(db)
    if categoryData.parent_id is not None:
        category = catalog_crud.get_category(
            category_id=categoryData.parent_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Родительская категория не найдена")
        if catalog_crud.category_has_products(category_id=categoryData.parent_id):
            if not categoryData.parent_products_to_child:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Укажите parent_products_to_child=True чтобы перенести продукты в новую категорию")
    db_image = save_image(upload_file=CategoryPicture, db=db,
                          user_id=db_user.id)
    db_category = catalog_crud.create_category(
        name=categoryData.name, parent_id=categoryData.parent_id, db_image=db_image)
    if categoryData.parent_products_to_child:
        catalog_crud.move_products(
            category_id=categoryData.parent_id, new_category_id=db_category.id)
    return set_new_category_info(db_category)


@categories_router.delete('/{category_id}', responses={**HTTP_401_UNAUTHORIZED}, status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, Authorize: AuthJWT = Depends(),
                    db: Session = Depends(get_db)):
    '''
    Удаляет категорию
    '''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    admin = CRUDUser(db).is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    crud_catalog.detele_category(category_id=category_id)


@categories_router.put('/{category_id}',
                       responses={**HTTP_401_UNAUTHORIZED},
                       response_model=CategoryInfo)
def update_category(categoryData: CategoryInfo,
                    category_id: int,
                    Authorize: AuthJWT = Depends(),
                    db: Session = Depends(get_db)):
    '''
    Создает категорию в каталоге если parent_id не задан или None, а если задан создает подкатегорию заданной категории или подкатегории
    '''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    admin = user_cruds.is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    db_category = crud_catalog.update_category(
        category=category, name=categoryData.name)
    return jsonable_encoder(db_category)


@categories_router.get('',
                       responses={**HTTP_401_UNAUTHORIZED},
                       response_model=List[Categories])
def get_categories(

    db: Session = Depends(get_db),
):
    "Возвращает список категорий"

    return CRUDCatalog(db).get_root_categories()


@categories_router.get('/{category_id}/products', response_model=List[CatalogProduct])
def get_products_from_category(category_id: int, order_by: settings.ProductSort = settings.ProductSort.price, order: settings.Order = settings.Order.desc, page: int = 1, db: Session = Depends(get_db)):
    "Товары из категории"
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    return crud_catalog.get_products_category(category_id=category_id,
                                              page=page, order_by=order_by, order=order)


@categories_router.post(
    '/{category_id}/products',
    responses={**HTTP_401_UNAUTHORIZED},
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    category_id: int, product_data: CreateProductForm,
    ProductPicture: UploadFile = File(...),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Создание товара'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    admin = user_cruds.is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")

    db_image_min, db_image = save_image(upload_file=ProductPicture, db=db,
                                        user_id=current_user_id, with_big=True)
    crud_product = CRUDProduct(db)
    db_product = crud_product.create_product(
        name=product_data.name,
        category_id=category_id,
        characteristics=product_data.characteristics,
        price=product_data.price,
        pic=db_image,
        pic_min=db_image_min,
        description=product_data.description
    )
    return db_product


@categories_router.get('/{category_id}/subcategories', response_model=Categories)
def get_category_info(category_id: int, db: Session = Depends(get_db)):
    "Информация о категории"
    category = CRUDCatalog(db).get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    return category


@categories_router.get('/{category_id}', response_model=CreatedCategory)
def get_category_info(category_id: int, db: Session = Depends(get_db)):
    "Информация о категории"
    category = CRUDCatalog(db).get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    return category


@categories_router.put('/{category_id}', response_model=CreateCategoryBase)
def update_category(category_id: int, category: CreateCategory, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    "Обновляет категорию"
    authorize.jwt_required()
    current_user_id = authorize.get_jwt_subject()
    admin = CRUDUser(db).is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    return crud_catalog.update_category(category=category, name=category.name)


@categories_router.get('/{category_id}/has-content', response_model=bool)
def has_content(category_id: int, db: Session = Depends(get_db)):
    "Проверяет наличие товаров или подкатегорий в категории"
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    return crud_catalog.has_content(category_id=category_id)


@categories_router.put('/{category_id}/move-products', status_code=status.HTTP_204_NO_CONTENT)
def move_products(category_id: int, new_category_id: int, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    "Перемещает товары из категории в другую"
    authorize.jwt_required()
    current_user_id = authorize.get_jwt_subject()
    user_cruds = CRUDUser(db)
    admin = user_cruds.is_admin(current_user_id)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="недостаточно прав")
    crud_catalog = CRUDCatalog(db)
    category = crud_catalog.get_category(category_id=category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="категория не найдена")
    new_category = crud_catalog.get_category(category_id=new_category_id)
    if not new_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="новая категория не найдена")
    crud_catalog.move_products(
        category_id=category_id, new_category_id=new_category_id)
