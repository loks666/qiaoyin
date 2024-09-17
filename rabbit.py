import pika
import json
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# RabbitMQ 连接参数
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

def create_rabbitmq_connection(exchange_name='device_exchange', queue_name='device_queue', routing_key='device.data'):
    """
    创建 RabbitMQ 连接并返回连接和通道。

    :param exchange_name: 交换机名称
    :param queue_name: 队列名称
    :param routing_key: 路由键
    :return: (connection, channel)
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # 声明交换机和队列
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
    return connection, channel

def produce(data, exchange_name=None, queue_name=None, routing_key=None):
    """
    生产消息到 RabbitMQ。

    :param data: 要发送的数据（应可序列化为 JSON）
    :param exchange_name: 交换机名称（可选）
    :param queue_name: 队列名称（可选）
    :param routing_key: 路由键（可选）
    """
    # 使用传入的参数或默认值
    exchange = exchange_name if exchange_name else os.getenv('EXCHANGE_NAME', 'device_exchange')
    queue = queue_name if queue_name else os.getenv('QUEUE_NAME', 'device_queue')
    routing = routing_key if routing_key else os.getenv('ROUTING_KEY', 'device.data')

    try:
        connection, channel = create_rabbitmq_connection(exchange, queue, routing)
        message = json.dumps(data)
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # 使消息持久化
            )
        )
        print(f"已发送消息到 RabbitMQ：{message}")
        connection.close()
    except Exception as e:
        print(f"发送消息到 RabbitMQ 时出现错误：{e}")

def consume(exchange_name=None, queue_name=None, routing_key=None):
    """
    从 RabbitMQ 中消费一条消息。

    :param exchange_name: 交换机名称（可选）
    :param queue_name: 队列名称（可选）
    :param routing_key: 路由键（可选）
    :return: 消费到的消息（Python 字典）或 None
    """
    # 使用传入的参数或默认值
    exchange = exchange_name if exchange_name else os.getenv('EXCHANGE_NAME', 'device_exchange')
    queue = queue_name if queue_name else os.getenv('QUEUE_NAME', 'device_queue')
    routing = routing_key if routing_key else os.getenv('ROUTING_KEY', 'device.data')

    try:
        connection, channel = create_rabbitmq_connection(exchange, queue, routing)
        method_frame, header_frame, body = channel.basic_get(queue=queue, auto_ack=False)
        if method_frame:
            message = json.loads(body)
            # 确认消息
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            print(f"已消费消息：{message}")
            connection.close()
            return message
        else:
            print("队列中没有消息")
            connection.close()
            return None
    except Exception as e:
        print(f"从 RabbitMQ 中消费消息时出现错误：{e}")
        return None
