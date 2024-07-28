from faker import Faker
from fastapi import APIRouter
from pprint import pprint
from scapy.layers.inet import *

from .. import common

net_message_router = APIRouter()


class PacketGenerator:
    def __init__(self, source_ip, dest_ip,source_port,dest_port,protocol):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_port = source_port
        self.dest_port = dest_port
        self.protocol = protocol

    def create_tcp_packet(self):
        return IP(src=self.source_ip, dst=self.dest_ip) / TCP(sport=self.source_port, dport=self.dest_port)

    def create_udp_packet(self, source_port=None, dest_port=None):
        return IP(src=self.source_ip, dst=self.dest_ip) / UDP(sport=self.source_port, dport=self.dest_port)

    def create_icmp_packet(self):
        return IP(src=self.source_ip, dst=self.dest_ip) / ICMP()

    def create_http_packet(self, data=None):
        if data is None:
            data = "GET / HTTP/1.0\r\n\r\n"
        return IP(src=self.source_ip, dst=self.dest_ip) / TCP(dport=80) / data

    def create_https_packet(self, data=None):
        if data is None:
            data = "GET / HTTP/1.0\r\n\r\n"
        return IP(src=self.source_ip, dst=self.dest_ip) / TCP(dport=443) / data

    def set_packet(self):
        if self.protocol == 'TCP':
            return self.create_tcp_packet()
        elif self.protocol == 'UDP':
            return self.create_udp_packet()
        elif self.protocol == 'ICMP':
            return self.create_icmp_packet()
        elif self.protocol == 'HTTP':
            return self.create_http_packet()
        elif self.protocol == 'HTTPS':
            return self.create_https_packet()

def generate_random_data():
    faker = Faker()

    # 定义可能的协议列表
    protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS']

    # 随机生成字典数据
    source_ip = faker.ipv4()
    dest_ip = faker.ipv4()
    source_port = random.randint(1, 65535)
    dest_port = random.randint(1,65535)
    protocol = random.choice(protocols)

    packet_generator = PacketGenerator(source_ip=source_ip,dest_ip=dest_ip,source_port=source_port,dest_port=dest_port,protocol=protocol)
    pack = packet_generator.set_packet()

    # data = {
    #     '源ip': faker.ipv4(),
    #     '目的ip': faker.ipv4(),
    #     '端口号': random.randint(1, 65535),
    #     '协议': random.choice(protocols),
    #     '数据包': os.urandom(random.randint(64, 1500)).hex()
    # }
    data = {
        '源ip': source_ip,
        '目的ip': dest_ip,
        '源端口号': source_port,
        "目的端口号":dest_ip,
        '协议': protocol,
        '数据包': str(pack)
    }

    return data

# 生成多个对应数据包
def set_more_data(nums = 200):
    return [generate_random_data() for _ in range(nums)]



#
# 返回网卡流量
@net_message_router.get("/network_traffic")
async def get_network_traffic():
    return common.dataReturn(1, "Get net message succeed", set_more_data(10))



if __name__ == '__main__':
    pprint((generate_random_data()))