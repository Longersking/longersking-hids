import time
import json
import asyncio
import threading
from queue import Queue
from traffic_monitor.traffic_sniffer import TrafficSniffer
from traffic_monitor.traffic_stats import deal_stats
from config import SERVER_URL
from utils import get_ip_address, send_data_to_server
from scapy.all import sniff, IP, TCP, UDP, ICMP

def sending_thread(queue, ip_address):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        if not queue.empty():
            current_stats = queue.get()
            loop.run_until_complete(send_data_to_server(SERVER_URL, ip_address, json.dumps(current_stats)))
        time.sleep(1)

def main():
    ip_address = get_ip_address()
    queue = Queue()

    sniff_thread = threading.Thread(target=deal_stats, args=(queue, None))
    send_thread = threading.Thread(target=sending_thread, args=(queue, ip_address))

    sniff_thread.start()
    send_thread.start()

    # sniff_thread.join()
    # send_thread.join()

if __name__ == "__main__":
    main()
