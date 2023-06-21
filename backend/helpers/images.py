import uuid
from backend.models.files import Image
from backend.core.config import settings
import io
from PIL import Image as pillow
import logging
import shutil
from fastapi import UploadFile, HTTPException
from backend.crud.crud_file import CRUDFile
from sqlalchemy.orm import Session
from pathlib import Path
logger = logging.getLogger(__name__)
supported_image_extensions = {
    ex for ex, f in pillow.registered_extensions().items() if f in pillow.OPEN}


def set_picture(data: dict, picture: Image, custom_key='picture'):
    if picture:
        data[custom_key] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', str(picture.id)])
    return data


def save_image(upload_file: UploadFile, db: Session, user_id: int, resize_image_options=(400, 400), bytes_io_file: io.BytesIO = None, with_big=False, detail_error_message="поврежденный файл"):
    if (not upload_file or not upload_file.filename) if not bytes_io_file else False:
        if with_big:
            return None, None
        return
    if bytes_io_file:
        originalFileName = bytes_io_file.name
    else:
        originalFileName = upload_file.filename
    originalFilePath = Path(originalFileName)
    suffix = originalFilePath.suffix
    if suffix.lower() not in supported_image_extensions:
        raise HTTPException(
            status_code=500, detail="Расширение изображения не поддерживается")
    if bytes_io_file:
        buf = bytes_io_file
    else:
        buf = io.BytesIO()
        shutil.copyfileobj(upload_file.file, buf)
        buf.seek(0)
    try:

        min_file = save_bytes_image(db=db,
                                    buf=buf, user_id=user_id, resize_image_options=resize_image_options)
        if with_big:
            return min_file, save_bytes_image(buf=buf, user_id=user_id, resize=False, db=db, resize_image_options=resize_image_options)
        return min_file
    except:
        raise HTTPException(status_code=500, detail=detail_error_message)


def save_bytes_image(buf, user_id: int, resize_image_options: tuple, db: Session, resize=True):
    image = pillow.open(buf)
    if resize:
        image.thumbnail(resize_image_options)
    image_model = CRUDFile(db).create_image(
        width=image.width, height=image.height, user_id=user_id)
    image.save('/'.join([settings.IMAGES_FOLDER,
                         str(image_model.id)+settings.IMAGES_EXTENTION]))
    return image_model


def image_id_to_url(image_id: uuid.UUID) -> str:
    return ''.join([settings.API_V1_STR, settings.UPLOADS_ROUTE, '/images/', str(image_id)])
