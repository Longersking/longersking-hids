from queue import Queue

class PacketProcessor:
    def __init__(self, string_matcher):
        self.string_matcher = string_matcher
        self.result_queue = Queue()

    def process_packet(self, packet):
        src_ip = packet['src_ip']
        dst_ip = packet['dst_ip']
        payload = packet['payload']

        matches = self.string_matcher.match(payload)

        result = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'payload': payload,
            'matches': matches
        }

        self.result_queue.put(result)
