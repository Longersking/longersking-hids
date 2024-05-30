from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.templating import Jinja2Templates
from data_handle.chart import Chart
from host_detection.sys_monitor import Monitor

# 配置路由
sys_message_router= APIRouter()

# 默认页面
template = Jinja2Templates(r"..\UI\app\views\templates")

# 绘制cpu水晶球
@sys_message_router.get("/cpu")
async def sys_message():
    m = Monitor()
    c = Chart()
    cpu_info = m.cpu()
    data = dict(
        cpu_liquid = c.liquid_html("cpu_avg","CPU平均使用率",cpu_info['cpu_avg'])
    )
    return cpu_info