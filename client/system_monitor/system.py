import psutil
import logging
from datetime import datetime

def td(tm):
    try:
        dt = datetime.fromtimestamp(tm)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logging.error(f"Error in td method: {e}")
        return ""

# 最近开机信息
def get_system_info():
    try:
        return td(psutil.boot_time())
    except Exception as e:
        logging.error(f"Error in lastest_start_time method: {e}")
        return ""

# 专门获取系统最近登录用户
def get_logined_users():
    try:
        users = psutil.users()
        data = [
            dict(
                name=v.name,
                terminal=v.terminal,
                host=v.host,
                started=td(v.started),
                pid=v.pid
            )
            for v in users
        ]
        return data
    except Exception as e:
        logging.error(f"Error in logined_users method: {e}")
        return []
