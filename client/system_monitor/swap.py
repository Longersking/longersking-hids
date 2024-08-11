import psutil
import logging
from .memory import byte_to_gb

# 获取交换内存区
def get_swap_info():
    try:
        info = psutil.swap_memory()
        data = dict(
            total=byte_to_gb(info.total),
            used=byte_to_gb(info.used),
            free=byte_to_gb(info.free),
            percent=info.percent
        )
        return data
    except Exception as e:
        logging.error(f"Error in swap_memory method: {e}")
        return {}
