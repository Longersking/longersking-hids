from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
template = Jinja2Templates(r"app/views/templates")

@router.get("/")
async def root(req: Request):
    return template.TemplateResponse("login.html", context={"request": req})

@router.get("/add", response_class=HTMLResponse)
async def add(req: Request):
    return template.TemplateResponse("user/add.html", context={"request": req})

# 后台框架
@router.get("/index", response_class=HTMLResponse)
async def add(req: Request):
    return template.TemplateResponse("index.html", context={"request": req})

# 后台首页
@router.get("/home", response_class=HTMLResponse)
async def add(req: Request):
    return template.TemplateResponse("home.html", context={"request": req})

@router.get("/ip/log", response_class=HTMLResponse)
async def log(req: Request):
    return template.TemplateResponse("ip/log.html", context={"request": req})

@router.get("/disabled_ip", response_class=HTMLResponse)
async def log(req: Request):
    return template.TemplateResponse("ip/disabled.html", context={"request": req})



# 用户路由
@router.get("/user/list", response_class=HTMLResponse)
async def log(req: Request):
    return template.TemplateResponse("user/list.html", context={"request": req})

@router.get("/user/logpage", response_class=HTMLResponse)
async def log(req: Request):
    return template.TemplateResponse("user/log.html", context={"request": req})

# 网络模块
@router.get("/network/monitor", response_class=HTMLResponse)
async def log(req: Request):
    return template.TemplateResponse("network/monitor.html", context={"request": req})