from backend.helpers.images import set_picture
from backend.models.products import Product
from backend.crud.crud_review import CRUDReview
from sqlalchemy.orm import Session


def get_product_json(db_product: Product, db: Session, add_reviews=True):
    product_data_obj = db_product.as_dict()
    product_data_obj = set_picture(product_data_obj, db_product.picture)
    product_data_obj = set_picture(
        product_data_obj, db_product.picture_min, custom_key='picture_min')
    if add_reviews:
        product_data_obj['reviews'] = CRUDReview(db).get_last_product_reviews(
            product_id=db_product.id, page=1)
    return product_data_obj
