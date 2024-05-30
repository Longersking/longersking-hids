# app/main.py
from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from UI.app.controllers.user_controller import user_router
from UI.app.controllers.system_message_controller import sys_message_router

app = FastAPI()

# 挂载静态资源
app.mount("/static", StaticFiles(directory="app/static"))

# 默认页面目录
template = Jinja2Templates(r"app\views\templates")

# 注册路由
app.include_router(user_router, prefix="/user")

app.include_router(sys_message_router, prefix="/sys_message")

# app.include_router(report_router, prefix="/report")


# 异步函数async
@app.get("/")
async def root(req: Request):
    return template.TemplateResponse("login.html", context={"request": req})



@app.get("/add", response_class=HTMLResponse)
async def add(req: Request):
    return template.TemplateResponse("add_user.html", context={"request": req})
