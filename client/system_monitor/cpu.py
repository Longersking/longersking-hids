import psutil
import logging

# 获取cpu信息
def get_cpu_info():
    try:
        cpu_times = psutil.cpu_times()
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_physic=psutil.cpu_count(logical=False),
            num_logic=psutil.cpu_count(logical=True),
            cpu_times={
                "user": cpu_times[0],
                "system": cpu_times[1],
                "idle": cpu_times[2],
                "interrupt": cpu_times[3],
                "dead": cpu_times[4],
            },

        )
        return data
    except Exception as e:
        logging.error(f"Error in cpu method: {e}")
        return {}