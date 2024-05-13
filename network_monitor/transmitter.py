import pika
import json
from config import RABBITMQ_HOST, RABBITMQ_QUEUE


class RabbitMQTransmitter:
    def __init__(self):
        # 初始化连接
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        # 连接到RabbitMQ
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            self.channel = self.connection.channel()

            # 确保队列存在
            self.channel.queue_declare(queue=RABBITMQ_QUEUE)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def transmit_data(self, data):
        if self.channel is None or self.connection is None:
            # 尝试重新连接
            self._connect()

        if self.channel is not None:
            try:
                # 将数据转换为JSON字符串
                json_data = json.dumps(data)

                # 发送数据
                self.channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=json_data)
            except pika.exceptions.AMQPError as e:
                print(f"Error while sending data: {e}")

    def close(self):
        if self.connection is not None:
            try:
                self.connection.close()
            except Exception as e:
                print(f"Error while closing connection: {e}")


# 使用示例
if __name__ == "__main__":
    transmitter = RabbitMQTransmitter()

    sample_data = {"key": "value"}
    transmitter.transmit_data(sample_data)

    # 关闭连接
    transmitter.close()
