# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from UI.app.controllers.user_controller import user_router
from UI.app.controllers.system_message_controller import sys_message_router
from UI.app.routers import templates

app = FastAPI()

# 挂载静态资源
app.mount("/static", StaticFiles(directory="app/static"))

# 注册路由
app.include_router(user_router, prefix="/user")

# 模板路由
app.include_router(templates.router)

app.include_router(sys_message_router, prefix="/sys_message")

