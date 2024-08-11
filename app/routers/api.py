from fastapi import APIRouter
from app.controllers import host_controller,menu_controller,user_controller,alert_controller,file_monitor_controller,packet_moniter_controller,websocket_controller

router = APIRouter()

# 主机路由
router.include_router(host_controller.router, prefix="/api/host", tags=["host"])

# 菜单路由
router.include_router(menu_controller.router, prefix="/api/menu", tags=["menu"])

# 用户路由
router.include_router(user_controller.user_router, prefix="/api/user", tags=["user"])

# 告警路由
router.include_router(alert_controller.router, prefix="/api/alert", tags=["user"])

# 文件路由
router.include_router(file_monitor_controller.router, prefix="/api/file_logs", tags=["user"])

# 数据包路由
router.include_router(packet_moniter_controller.router, prefix="/api/packet", tags=["user"])


# ws api 路由
router.include_router(websocket_controller.websocket_router, prefix="/api/ws", tags=["user"])
