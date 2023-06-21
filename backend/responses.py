from backend.schemas.error import HTTP_401_UNAUTHORIZED as HTTP_401_Model
from fastapi import status
HTTP_401_UNAUTHORIZED = {status.HTTP_401_UNAUTHORIZED: {
    "model": HTTP_401_Model}}
