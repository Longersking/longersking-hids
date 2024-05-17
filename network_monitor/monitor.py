import queue
import time
import threading
from capture import start_capture_thread
from filter import IPFilterStrategy, PortFilterStrategy
from parser import PacketParser
from transmitter import PacketTransmitter
import config


def packet_processing_thread(packet_queue, output_queue, filter_strategy):
    parser = PacketParser()
    transmitter = PacketTransmitter(output_queue)

    while True:
        packet = packet_queue.get()
        if packet is None:
            break
        if filter_strategy.apply_filter(packet):
            parsed_packet = parser.parse_packet(packet)
            transmitter.transmit_packet(parsed_packet)


def main():
    packet_queue = queue.Queue(config.OUTPUT_QUEUE_SIZE)
    output_queue = queue.Queue()

    # 启动数据包捕获线程
    capture_thread = start_capture_thread(config.INTERFACE, packet_queue)

    # 选择过滤策略
    filter_strategy = IPFilterStrategy(config.FILTER_IP_ADDRESS)

    # 启动数据包处理线程
    processing_thread = threading.Thread(target=packet_processing_thread,
                                         args=(packet_queue, output_queue, filter_strategy))
    processing_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        packet_queue.put(None)
        capture_thread.join()
        processing_thread.join()


if __name__ == "__main__":
    main()
