import asyncio
import websockets
import json
from typing import Dict,Any


from sys_monitor import Monitor
from agent import common


# 获取当前cpu信息
async def cpu_message( ) -> Dict[str, Any]:
    """
        获取当前 CPU 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 CPU 信息。

        Returns:
            Dict[str, Any]: 返回包含 CPU 信息的字典。
    """
    m = Monitor()

    cpu_info = m.cpu()

    return common.dataReturn(1, msg="CPU message", data=cpu_info)



# 获取当前内存交互信息

async def mem_message( ) -> Dict[str, Any]:
    """
        获取当前 内存 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 内存 信息。

        Returns:
            Dict[str, Any]: 返回包含 内存 信息的字典。
    """
    m = Monitor()

    mem_info = m.mem()

    return common.dataReturn(1, msg="MEM message", data=mem_info)


# 获取当前交互内存区信息
async def swap_memory_message( ) -> Dict[str, Any]:
    """
        获取当前 交互分区 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 交互分区 信息。

        Returns:
            Dict[str, Any]: 返回包含 交互分区 信息的字典。
    """
    m = Monitor()

    swap_memory_info = m.swap_memory()

    return common.dataReturn(1, msg="SWAP_MEMORY message", data=swap_memory_info)


# 获取当前磁盘信息
async def disk_message( ) -> Dict[str, Any]:
    """
        获取当前 磁盘 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 磁盘 信息。

        Returns:
            Dict[str, Any]: 返回包含 磁盘 信息的字典。
    """
    m = Monitor()

    disk_info = m.disk()

    return common.dataReturn(1, msg="DISK message", data=disk_info)


# 获取当前网卡信息

async def net_message( ) -> Dict[str, Any]:
    """
        获取当前 网卡 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 网卡 信息。

        Returns:
            Dict[str, Any]: 返回包含 网卡 信息的字典。
    """
    m = Monitor()

    net_info = m.net()

    return common.dataReturn(1, msg="NET message", data=net_info)


# 获取当前主机用户最近登录信息
async def logined_users( ) -> Dict[str, Any]:
    """
        获取当前 主机用户登录 信息的异步接口。

        Args:
            m (Monitor): Monitor 类的实例，用于获取 主机用户登录 信息。

        Returns:
            Dict[str, Any]: 返回包含 主机用户登录 信息的字典。
    """
    m = Monitor()

    logined_users = m.logined_users()

    return common.dataReturn(1, msg="LOGINED_USERS", data=logined_users)

async def load_info():
    cpu = await cpu_message()
    cpu = cpu['data']
    mem = await mem_message()
    mem = mem['data']
    swap=await swap_memory_message()
    swap = swap['data']
    disk = await  disk_message()
    disk = disk['data']
    net = await  net_message()
    net = net['data']
    return common.dataReturn(1, "负载信息", {
        "cpu":cpu,
        "mem":mem,
        "swap":swap,
        "disk":disk,
        "net":net
    })

async def report_system_info(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            system_info = await load_info()
            await websocket.send(json.dumps(system_info))
            await asyncio.sleep(10)  # 每10秒发送一次系统信息

if __name__ == "__main__":
    server_uri = "ws://192.168.100.102:8004/test/load_info"  # 替换为实际服务器的IP和端口
    asyncio.get_event_loop().run_until_complete(report_system_info(server_uri))
