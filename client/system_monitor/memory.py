import psutil
import logging

def byte_to_gb(data, key=""):
    if key == "percent":
        return data
    return round(data / (1024 ** 3), 2)

# 获取内存信息
def get_memory_info():
    try:
        info = psutil.virtual_memory()
        data = dict(
            total=byte_to_gb(info.total),
            used=byte_to_gb(info.used),
            free=byte_to_gb(info.free),
            percent=info.percent
        )
        return data
    except Exception as e:
        logging.error(f"Error in mem method: {e}")
        return {}
