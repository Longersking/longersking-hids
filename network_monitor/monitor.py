import threading
from capture import capture_packets
from parser import parse_packet
from transmitter import RabbitMQTransmitter
import time

# 用于控制线程的停止
stop_event = threading.Event()

# 捕获数据包的处理函数
def packet_handler(packet):
    try:
        # 解析数据包
        parsed_data = parse_packet(packet)

        # 传输解析后的数据
        transmitter.transmit_data(parsed_data)
    except Exception as e:
        print(f"Error processing packet: {e}")

# 主监控函数
def start_monitoring():
    # 初始化数据传输器
    global transmitter
    transmitter = RabbitMQTransmitter()

    # 使用多线程捕获数据包
    capture_thread = threading.Thread(target=capture_packets, args=(packet_handler,))
    capture_thread.start()

    # 等待一定时间后停止捕获
    return capture_thread

# 线程停止机制
def stop_monitoring(capture_thread):
    stop_event.set()  # 停止捕获
    capture_thread.join()  # 等待线程结束
    transmitter.close()  # 关闭传输器


if __name__ == "__main__":
    # 启动监控
    capture_thread = start_monitoring()

    try:
        # 模拟运行10秒后停止监控
        time.sleep(10)
        stop_monitoring(capture_thread)
    except KeyboardInterrupt:
        # 支持通过 Ctrl+C 终止监控
        stop_monitoring(capture_thread)
