import asyncio
import threading
from queue import Queue
import config
from utils import get_ip_address, send_data_to_server,receive_commands
from traffic_monitor.traffic_stats import deal_stats
from thread import process_monitor_thread, system_load_thread, file_monitor_thread
from monitor.packet_monitor import PacketMonitor
from handler.rule_manager import RuleManager
from handler.string_matcher import StringMatcher
from handler.IP_block_handler import IPBlocker  # 导入IPBlocker类
import websockets
import json



def main():
    ip_address = get_ip_address()
    rule_manager = RuleManager("rule.json")  # 规则管理器
    rules = rule_manager.get_enabled_rules()  # 启用的规则
    matcher = StringMatcher(rules)  # 字符串匹配器
    queue = Queue()
    sys_queue = Queue()
    process_queue = Queue()
    file_alarm_queue = Queue()  # 添加警报队列
    packet_queue = Queue()  # 添加包捕获队列

    # 启动数据采集线程
    sniff_thread = threading.Thread(target=deal_stats, args=(queue, None))  # 流量采集线程
    load_thread = threading.Thread(target=system_load_thread, args=(sys_queue, ip_address))  # 系统负载采集线程
    process_thread = threading.Thread(target=process_monitor_thread,
                                      args=(config.get_config()["process_to_monitor"], process_queue))  # 进程监控线程
    file_thread = threading.Thread(target=file_monitor_thread,
                                   args=(file_alarm_queue, config.MONITORED_PATHS))  # 文件监控线程
    pack_monitor = PacketMonitor("eth0", packet_queue, matcher)

    sniff_thread.start()
    load_thread.start()
    process_thread.start()
    file_thread.start()
    pack_monitor.start()

    # 启动 WebSocket 命令接收线程
    ip_blocker = IPBlocker()
    ws_receive_thread = threading.Thread(target=asyncio.run, args=(receive_commands(config.SERVER_URL, ip_blocker),))
    ws_receive_thread.start()

    # 启动 WebSocket 发送线程
    asyncio.run(send_data_to_server(config.SERVER_URL, ip_address, traffic_stats=queue, system_load=sys_queue,
                                    process_data=process_queue, file_change=file_alarm_queue,
                                    packet_monitor=packet_queue))

    sniff_thread.join()
    load_thread.join()
    process_thread.join()
    file_thread.join()
    ws_receive_thread.join()


if __name__ == "__main__":
    main()

