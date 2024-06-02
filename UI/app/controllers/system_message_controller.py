from fastapi import APIRouter
from typing import Dict,Any
import json


from host_detection.sys_monitor import Monitor
from .. import common

# 配置路由
sys_message_router= APIRouter()

# 获取当前cpu信息
@sys_message_router.get("/cpu")
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

    return common.dataReturn(1,msg="CPU message",data=cpu_info)


# 获取当前内存交互信息
@sys_message_router.get("/mem")
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

    return common.dataReturn(1,msg="MEM message",data=mem_info)


# 获取当前交互内存区信息
@sys_message_router.get("/swap_memory")
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

    return common.dataReturn(1,msg="SWAP_MEMORY message",data=swap_memory_info)


# 获取当前磁盘信息
@sys_message_router.get("/disk")
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

    return common.dataReturn(1,msg="DISK message",data=disk_info)


# 获取当前网卡信息
@sys_message_router.get("/net")
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

    return common.dataReturn(1,msg="NET message",data=net_info)


# 获取当前主机用户最近登录信息
@sys_message_router.get("/logined_users")
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

    return common.dataReturn(1,msg="LOGINED_USERS",data=logined_users)

@sys_message_router.get("/load_info")
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
    return common.dataReturn(1,"负载信息",{
        "cpu":cpu,
        "mem":mem,
        "swap":swap,
        "disk":disk,
        "net":net
    })







