from typing import Any, List
from backend.db.base_class import Base

from backend.core.config import settings


class CRUDBase:
    def __init__(self, db) -> None:
        self.db = db

    def get(self, id: Any, model):
        return self.db.query(model).filter(model.id == id).first()

    def get_multi(
            self, model, page: int, page_size: int = settings.REVIEWS_PER_PAGE) -> List:
        end = page * page_size
        return self.db.query(model).slice(end-page_size, end).all()

    def update(self, model):
        self.db.commit()
        self.db.refresh(model)
        return model

    def create(self,  model):
        self.db.add(model)
        self.update(model)
        return model

    def delete(self, model):
        self.db.delete(model)
        self.db.commit()
