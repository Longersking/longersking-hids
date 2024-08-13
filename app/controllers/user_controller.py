# controllers/user_controller.py
from datetime import timedelta
from typing import Union
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from starlette.requests import Request
from utils.security import get_password_hash, create_access_token, verify_password, SECRET_KEY, ALGORITHM, \
    ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme
from ..models.event import UserLog
from ..models.user import User
from ..models.database import get_db
from .. import common
from datetime import datetime
from app.schemas.user import UserCreate,UserInfo
# 注册用户路由
user_router = APIRouter()


@user_router.post("/addUser", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 检测用户是否重复
    if db.query(User).filter(User.username == user_data.username).first():
        return common.dataReturn(1, '用户已存在')

    # 创建用户并保存到数据库
    user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role,
        create_time = user_data.create_time
    )
    # 添加表
    db.add(user)
    db.commit()
    # 刷新表
    db.flush(user)
    return common.dataReturn(1, '添加用户成功', user)


async def add_user_log(user_id: int, username: str, ip_address: str, db: Session = Depends(get_db)):
    login_record = UserLog(uid=user_id, username=username, ip=ip_address, login_time=datetime.now())
    db.add(login_record)
    try:
        db.commit()
        db.refresh(login_record)
    except Exception as e:
        return common.dataReturn(-1, "error", e)


# 用户登录
@user_router.post("/login")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """
        表单传输数据
        x-www-form-urlencoded
    """
    ip_address = request.client.host
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        return common.dataReturn(0, '用户名或密码错误', user)
    res = await add_user_log(user_id=user.id, username=user.username, ip_address=ip_address, db=db)
    access_token_expire = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return common.dataReturn(1, 'Login succeed', {"access_token": access_token, "token_type": "bearer"})


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
            return common.dataReturn(-1, "未登录")
    except JWTError:
        return common.dataReturn(-2, "tokne验证失败")
        # raise credentials_exception

    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user:
        # raise credentials_exception
        return common.dataReturn(-3, "用户不存在")
    return common.dataReturn(1, "获取成功", user)


# 获取当前用户信息
async def get_current_user(current_user: User = Depends(get_user)):
    return current_user


# 前端交互接口
@user_router.get("/userMessage")
async def get_current_user_message(current_user: User = Depends(get_current_user)):
    return common.dataReturn(1, 'Get current user message', data=current_user)


# 添加用户
class UserCreate(BaseModel):
    username: Union[str, int]
    # email: str
    password: Union[str, int]
    role: str = "user"


@user_router.post("/addUser", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 检测用户是否重复
    if db.query(User).filter(User.username == user_data.username).first():
        return common.dataReturn(0, 'User already exists')

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
    return common.dataReturn(1, 'Add user succeed', user)


# 用户登录
async def get_user_log(user_id: int, username: str, ip_address: str, db: Session = Depends(get_db)):
    login_record = UserLog(user_id=user_id, username=username, ip_address=ip_address, login_time=datetime.utcnow())
    db.add(login_record)
    db.commit()
    db.refresh(login_record)


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

        return common.dataReturn(1, msg="ChangePassword succeed")

    except Exception as e:
        db.rollback()  # 确保在异常情况下回滚事务
        return common.dataReturn(0, msg="Error")


# 删除用户
@user_router.get("/deleteUser/{username}", response_model=dict)
async def delete_user(
        username: str,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    if current_user.role != "admin" or not current_user:
        # raise HTTPException(status_code=403, detail="非法用户越权，已记录日志")
        return common.dataReturn(0, msg="Hacker attack,had recorded")
    else:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            # raise HTTPException(status_code=404, detail="未找到此用户")
            return common.dataReturn(0, msg="Can't find this user!")

        db.delete(user)
        db.commit()

        return common.dataReturn(1, msg="Delete user succeed")


@user_router.get("/getList", response_model=dict)
async def getList(page: int = 1, db: Session = Depends(get_db)):
    userList = db.query(User).order_by(desc(User.id)).limit(10).offset(10 * (page - 1)).all()
    count = db.query(User).count()
    user_list = [
        UserInfo(id=item.id, username=item.username, disabled=item.disabled, create_time=str(item.create_time),
                 avatar=item.avatar, role=item.role) for item in
        userList]
    return common.dataReturn(1, msg="userlist", data={"data": user_list, "total": count})


@user_router.get("/delUser")
async def delUserBtId(uid: int, db: Session = Depends(get_db)):
    # 通过ID删除用户
    user = db.query(User).filter(User.id == uid).first()
    db.delete(user)
    try:
        db.commit()
        return common.dataReturn(1, "删除成功")
    except Exception as e:
        return common.dataReturn(-1, "删除失败", str(e))


@user_router.get("/disableUser")
async def delUserBtId(uid: int, db: Session = Depends(get_db)):
    # 通过ID删除用户
    user = db.query(User).filter(User.id == uid).first()
    user.disabled = 1
    try:
        db.commit()
        return common.dataReturn(1, "禁用成功")
    except Exception as e:
        return common.dataReturn(-1, "禁用失败", str(e))


@user_router.get("/allowUser")
async def delUserBtId(uid: int, db: Session = Depends(get_db)):
    # 通过ID删除用户
    user = db.query(User).filter(User.id == uid).first()
    user.disabled = 0
    try:
        db.commit()
        return common.dataReturn(1, "解封成功")
    except Exception as e:
        return common.dataReturn(-1, "解封失败", str(e))


class userInfo(BaseModel):
    username: str
    oldpass: str = None
    avatar: str = None
    newpass: str = None


@user_router.post("/updateInfo")
async def delUserBtId(info: userInfo, db: Session = Depends(get_db)):
    # 修改用户信息
    user = db.query(User).filter(User.username == info.username).first()
    if info.oldpass != None and info.oldpass != "" and not verify_password(info.oldpass, user.hashed_password):
        return common.dataReturn(-1, "原密码不正确")
    else:
        if info.newpass != None and info.newpass != "":
            user.hashed_password = get_password_hash(info.newpass)

    if info.avatar != None:
        user.avatar = info.avatar

    try:
        db.commit()
        return common.dataReturn(1, "修改成功！")
    except Exception as e:
        return common.dataReturn(-2, "修改失败", str(e))


class LogInfo(BaseModel):
    id: int
    uid: int
    ip: str
    username: str
    login_time: str


@user_router.get("/log",response_model=dict)
async def getLog(page: int = 1, db: Session = Depends(get_db)):
    logList = db.query(UserLog).order_by(desc(UserLog.id)).limit(10).offset(10 * (page - 1)).all()
    count = db.query(UserLog).count()
    log_list = [
        LogInfo(id=item.id, uid=item.uid,username=item.username, login_time=str(item.login_time),
                ip=item.ip) for item in logList]
    return common.dataReturn(1, msg="userloglist", data={"data": log_list, "total": count})
