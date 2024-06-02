# 文件路径: /mnt/data/main.py

import time
from capture import capture_on_interfaces

from host_detection import sys_monitor


def get_network_interfaces():
    # 根据系统获取所有网卡接口
    # 示例：返回固定的网卡接口列表
    sys_monitor.Monitor().net()
    network_interfaces = [net_int["name"] for net_int in sys_monitor.Monitor().net() ]
    return network_interfaces


def main():
    interfaces = get_network_interfaces()

    while True:
        try:
            capture_on_interfaces(interfaces)
        except KeyboardInterrupt:
            print("Stopping capture...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # 短暂休息后重试


if __name__ == "__main__":
    main()
