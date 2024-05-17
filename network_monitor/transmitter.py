import json
import queue

class PacketTransmitter:
    def __init__(self, output_queue):
        self.output_queue = output_queue

    def transmit_packet(self, packet_data):
        # 将数据包转换为 JSON 格式并传输
        packet_json = json.dumps(packet_data)
        self.output_queue.put(packet_json)

def start_transmitter_thread(output_queue):
    transmitter = PacketTransmitter(output_queue)
    transmitter_thread = threading.Thread(target=transmitter.transmit_packet)
    transmitter_thread.start()
    return transmitter_thread
