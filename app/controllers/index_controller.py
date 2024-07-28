from jose import jwt, JWTError
from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.security import get_password_hash, create_access_token, verify_password, SECRET_KEY, ALGORITHM, \
    ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from ..models.user import User
from ..models.database import get_db
from datetime import timedelta
from typing import Union
from .. import common

index_router = APIRouter()

# @index_router.get("/index")
# async def index():