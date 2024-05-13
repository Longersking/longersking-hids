# config.py
import os

# 捕获的网络接口
NETWORK_INTERFACE = "WLAN"

# 默认过滤规则
BPF_FILTER = "tcp or udp"

# 消息队列配置
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = "network_traffic"

