import time

import psutil
import logging
from .memory import byte_to_gb

# 获取磁盘信息
def get_disk_info():
    try:
        info = psutil.disk_partitions()
        io_start = psutil.disk_io_counters()
        time.sleep(1)
        io_end = psutil.disk_io_counters()
        data = [
            dict(
                device=v.device,
                mountpoint=v.mountpoint,
                fstype=v.fstype,
                opts=v.opts,
                used={
                    k: byte_to_gb(v, k)
                    for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
                },
                io={
                    "read_mb_s": (io_end.read_bytes-io_start.read_bytes) / 1024 / 1024,
                    "write_mb_s": (io_end.write_bytes-io_start.write_bytes) / 1024 / 1024,
                    "read_times_s" : (io_end.read_count-io_start.read_count),
                    "write_times_s" : (io_end.write_count-io_start.write_count),
                }
            )
            for v in info
        ]
        return data
    except Exception as e:
        logging.error(f"Error in disk method: {e}")
        return []
print(get_disk_info())