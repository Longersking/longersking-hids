# utils/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Union


ACCESS_TOKEN_EXPIRE_MINUTES = 3000
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "fb1cf684307ba367175cf472bd9cc0359b28289a40597654b3f0839ccf06e25f"
ALGORITHM = "HS256"
# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 密码哈希
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#创建token
# 创建 JWT 令牌
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)





