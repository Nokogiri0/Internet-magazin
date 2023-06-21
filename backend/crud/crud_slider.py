from datetime import datetime
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.models.slider import Slide
from backend.crud.crud_file import CRUDFile
from sqlalchemy import or_


class CRUDSlider(CRUDBase):
    def create_slide(self, name: str, open_date: datetime, close_date: datetime, url: str, picture: Image, position: int, is_active: bool) -> Slide:
        slide = Slide(name=name, open_date=open_date, close_date=close_date,
                      url=url, picture=picture, position=position, is_active=is_active)
        return self.create(slide)

    def update_slide(self, slide: Slide, name: str, open_date: datetime, close_date: datetime, url: str, picture: Image, position: int, is_active: bool) -> Slide:
        slide.name = name
        slide.open_date = open_date
        slide.close_date = close_date
        slide.url = url
        if picture:
            CRUDFile(self.db).replace_old_picture(
                model=slide, new_picture=picture)
        slide.position = position
        slide.is_active = is_active
        return self.update(slide)

    def get_slide_by_id(self, slide_id) -> Slide | None:
        return self.get(model=Slide, id=slide_id)

    def delete_slide_by_id(self, slide) -> None:
        self.delete(model=slide)

    def get_active_slides(self) -> list[Slide]:
        now = datetime.now()
        return self.db.query(Slide).filter(Slide.is_active == True).filter(Slide.open_date <= now, or_(Slide.close_date.is_(None), Slide.close_date >= now)).order_by(Slide.position.desc(), Slide.open_date.desc()).all()
