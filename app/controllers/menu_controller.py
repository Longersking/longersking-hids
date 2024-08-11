from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.database import get_db
from app.models.user import User
from app.models.menu import Menu
from app.models.permission_group import PermissionGroup
from app.controllers.user_controller import get_current_user
from app.common import dataReturn
router = APIRouter()


def get_user_permission_group(user: User, db: Session):
    if user['data'].role == 'admin':
        group_name = '管理员'
    else:
        group_name = '用户'

    permission_group = db.query(PermissionGroup).filter(PermissionGroup.name == group_name).first()
    return permission_group


@router.get("/get")
def get_menu(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    permission_group = get_user_permission_group(current_user, db)
    menu_ids = permission_group.menu_nodes
    menus = db.query(Menu).filter(Menu.id.in_(menu_ids)).all()

    menu_dict = {menu.id: menu for menu in menus}
    result = []

    for menu in menus:
        if menu.parent_id is None:
            menu_data = {
                "id": menu.id,
                "name": menu.name,
                "icon": menu.icon,
                "child": []
            }
            result.append(menu_data)

    for menu in menus:
        if menu.parent_id is not None:
            parent = menu_dict[menu.parent_id]
            parent_data = next(item for item in result if item["id"] == parent.id)
            parent_data["child"].append({
                "id": menu.id,
                "name": menu.name,
                "icon": menu.icon,
                "url": menu.url
            })

    return dataReturn(1,"获取成功",result)
