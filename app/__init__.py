# app/__init__.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.controllers.user_controller import user_router
from app.controllers.ip_disabled import ip_route
from app.controllers.system_message_controller import sys_message_router
from app.controllers.net_message_controller import net_message_router
from app.controllers.test_ws_controller import test_router
from app.routers import templates



def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8004",
        "http://127.0.0.1",
        "http://127.0.0.1:8004",
        # 添加其他允许的来源
    ]

    # 挂载静态资源
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # 跨域设置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有源
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有头
    )

    # 注册路由
    app.include_router(user_router, prefix="/user")
    app.include_router(sys_message_router, prefix="/sys_message")
    app.include_router(net_message_router, prefix="/net_message")
    app.include_router(test_router, prefix="/test")
    app.include_router(ip_route, prefix="/ip")
    app.include_router(templates.router)

    return app
