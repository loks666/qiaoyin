import pika
import json
import asyncio
import websockets
from websockets import WebSocketServerProtocol

# RabbitMQ 连接参数
rabbitmq_host = '60.204.169.49'
rabbitmq_port = 1883  # 修改为 Docker 容器映射的本地端口 1883
rabbitmq_user = 'admin'  # 修改为 Docker 中设置的用户名
rabbitmq_password = 'qiaoyin'  # 修改为 Docker 中设置的密码

# WebSocket 服务器地址和端口
websocket_host = 'localhost'
websocket_port = 8765

# 建立 RabbitMQ 连接和通道
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
)
channel = connection.channel()

# 声明交换机和队列
exchange_name = 'device_exchange'
queue_name = 'device_queue'
routing_key = 'device.data'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

async def websocket_handler(websocket: WebSocketServerProtocol, path: str):
    """
    WebSocket 处理程序，接收设备发送的 JSON 数据，并将数据推送到 RabbitMQ。
    """
    print(f"设备已连接: {path}")
    try:
        async for message in websocket:
            # 假设设备发送的消息是 JSON 格式
            try:
                data = json.loads(message)
                print(f"接收到设备数据: {data}")
                # 将接收到的消息发送到 RabbitMQ
                send_to_rabbitmq(data)
            except json.JSONDecodeError:
                print(f"接收到的消息不是有效的 JSON: {message}")
    except websockets.ConnectionClosed:
        print("设备已断开连接")

def send_to_rabbitmq(data):
    """
    将数据发送到 RabbitMQ。
    """
    message = json.dumps(data)
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # 使消息持久化
        )
    )
    print(f"已发送消息到 RabbitMQ：{message}")

async def start_websocket_server():
    """
    启动 WebSocket 服务器。
    """
    async with websockets.serve(websocket_handler, websocket_host, websocket_port):
        print(f"WebSocket 服务器已启动，等待设备连接... (ws://{websocket_host}:{websocket_port})")
        await asyncio.Future()  # 保持 WebSocket 服务器运行

if __name__ == "__main__":
    try:
        # 启动 WebSocket 服务器
        asyncio.get_event_loop().run_until_complete(start_websocket_server())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("服务器关闭中...")
    finally:
        # 关闭 RabbitMQ 连接
        connection.close()
        print("RabbitMQ 连接已关闭")
