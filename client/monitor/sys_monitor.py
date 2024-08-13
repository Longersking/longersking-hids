from datetime import datetime

import psutil
from pprint import pprint

from agent.handler.exception_handler import exception_handler_for_class

# 定义一个专门用于获取系统信息的类
@exception_handler_for_class
class SysMonitor(object):
    # 单位换算
    def byte_to_gb(self, data, key=""):
        if key == "percent":
            return data
        return round(data / (1024 ** 3), 2)

    # 获取cpu信息
    def cpu(self):
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_physic=psutil.cpu_count(logical=False),
            num_logic=psutil.cpu_count(logical=True)
        )
        return data

    # 获取内存信息
    def mem(self):
        info = psutil.virtual_memory()
        data = dict(
            total=self.byte_to_gb(info.total),
            used=self.byte_to_gb(info.used),
            free=self.byte_to_gb(info.free),
            percent=info.percent
        )
        return data

    # 获取交换内存区
    def swap_memory(self):
        info = psutil.swap_memory()
        data = dict(
            total=self.byte_to_gb(info.total),
            used=self.byte_to_gb(info.used),
            free=self.byte_to_gb(info.free),
            percent=info.percent
        )
        return data

    # 获取磁盘信息
    def disk(self):
        info = psutil.disk_partitions()
        data = [
            dict(
                device=v.device,
                mountpoint=v.mountpoint,
                fstype=v.fstype,
                opts=v.opts,
                used={
                    k: self.byte_to_gb(v, k)
                    for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
                }
            )
            for v in info
        ]
        return data

    # 获取网卡信息
    def net(self):
        addr = psutil.net_if_addrs()
        addr_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name == "AF_INET"
            ][0]
            for k, v in addr.items()
        }
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addr_info[k]
            )
            for k, v in io.items()
        ]
        return data

    # 时间戳转化为时间字符串的方式
    def td(self, tm):
        dt = datetime.fromtimestamp(tm)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # 最近开机信息
    def lastest_start_time(self):
        return self.td(psutil.boot_time())

    # 专门获取系统最近登录用户
    def logined_users(self):
        users = psutil.users()
        data = [
            dict(
                name=v.name,
                terminal=v.terminal,
                host=v.host,
                started=self.td(v.started),
                pid=v.pid
            )
            for v in users
        ]
        return data

if __name__ == '__main__':
    test = SysMonitor()
    pprint([net_name["name"] for net_name in test.net()])

