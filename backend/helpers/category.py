from typing import List
from backend.helpers.images import image_id_to_url
from backend.models.products import Category
from backend.crud.crud_catalog import CRUDCatalog
from sqlalchemy.orm import Session


def set_category_info(category: Category, page: int, db: Session):
    category_obj = {'id': category.id, 'name': category.name}
    category_obj['picture'] = image_id_to_url(category.picture.id)
    category_obj['products'] = CRUDCatalog(db).get_products_category(
        category_id=category.id, page=page)

    return category_obj


def set_category_info_no_products(category: Category, sub_categories: List[Category] = None):
    category_obj = {'id': category.id, 'name': category.name}
    category_obj['picture'] = image_id_to_url(category.picture.id)
    if sub_categories:
        category_obj['children'] = sub_categories
    return category_obj


def set_new_category_info(category: Category):
    category_obj = {'id': category.id, 'name': category.name}
    category_obj['picture'] = image_id_to_url(category.picture.id)
    return category_obj
