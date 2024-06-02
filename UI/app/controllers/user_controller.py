# controllers/user_controller.py
from datetime import timedelta
from typing import Union

from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils.security import get_password_hash, create_access_token, verify_password, SECRET_KEY, ALGORITHM, \
    ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from ..models.user import User
from ..models.database import get_db
from .. import common

from sqlalchemy.ext.declarative import declarative_base

# 注册用户路由
user_router = APIRouter()

# 内部接口调用
# 获取用户信息
async def get_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user


# 获取当前用户信息
async def get_current_user(current_user: User = Depends(get_user)):
    return current_user


# 前端交互接口
@user_router.get("/userMessage")
async def get_current_user_message(current_user: User = Depends(get_current_user)):
    return common.dataReturn(1, 'Get current user message',data=current_user)


# 添加用户
class UserCreate(BaseModel):
    username: Union[str,int]
    # email: str
    password: Union[str,int]
    role: str = "user"


@user_router.post("/addUser", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # 检测用户是否重复
    if db.query(User).filter(User.username == user_data.username).first():
        return common.dataReturn(0,'User already exists')

    # 创建用户并保存到数据库
    user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    # 添加表
    db.add(user)
    db.commit()
    # 刷新表
    db.flush(user)
    return common.dataReturn(1,'Add user succeed',user)


# 用户登录
@user_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """
        表单传输数据
        x-www-form-urlencoded
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return common.dataReturn( 0, '用户名或密码错误', user)

    access_token_expire = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return common.dataReturn(1,'Login succeed',{"access_token": access_token, "token_type": "bearer"})


# 更改密码
class ChangePassword(BaseModel):
    old_password: str
    new_password: str


@user_router.put("/changePassword")
async def changePassword(
        password_data: ChangePassword,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        current_user = db.merge(current_user)

        if not verify_password(password_data.old_password, current_user.hashed_password):
            # raise HTTPException(status_code=400, detail="Password incorrect")
            return common.dataReturn(0, msg="Password incorrect")

        current_user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()
        db.refresh(current_user)

        return common.dataReturn(1,msg="ChangePassword succeed")

    except Exception as e:
        db.rollback()  # 确保在异常情况下回滚事务
        return common.dataReturn( 0,msg="Error")



# 删除用户
@user_router.get("/deleteUser/{username}", response_model=dict)
async def delete_user(
        username: str,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    if current_user.role != "admin" or not current_user:
        # raise HTTPException(status_code=403, detail="非法用户越权，已记录日志")
        return common.dataReturn( 0, msg="Hacker attack,had recorded")
    else:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            # raise HTTPException(status_code=404, detail="未找到此用户")
            return common.dataReturn( 0, msg="Can't find this user!")

        db.delete(user)
        db.commit()

        return common.dataReturn(1,msg="Delete user succeed")
