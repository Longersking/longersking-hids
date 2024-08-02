from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.user_controller import user_router
from app.controllers.ip_disabled import ip_route
from app.controllers.system_message_controller import sys_message_router
from app.controllers.net_message_controller import net_message_router
from app.controllers.websocket_controller import websocket_router  # 引入 WebSocket 路由
from app.routers import templates


def create_app() -> FastAPI:
    app = FastAPI()

    # 挂载静态资源
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # 注册路由
    app.include_router(user_router, prefix="/user")
    app.include_router(sys_message_router, prefix="/sys_message")
    app.include_router(net_message_router, prefix="/net_message")
    app.include_router(ip_route, prefix="/ip")
    app.include_router(templates.router)
    app.include_router(websocket_router)  # 注册 WebSocket 路由

    return app
