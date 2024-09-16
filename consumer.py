import pika
import json

# RabbitMQ 连接参数
rabbitmq_host = '60.204.169.49'  # 远程 RabbitMQ 服务器的地址
rabbitmq_port = 1883  # RabbitMQ 的 AMQP 端口
rabbitmq_user = 'admin'  # RabbitMQ 的用户名
rabbitmq_password = 'qiaoyin'  # RabbitMQ 的密码

# 建立连接和通道
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
)
channel = connection.channel()

# 声明交换机和队列
exchange_name = 'device_exchange'
queue_name = 'device_queue'
routing_key = 'device.data'

# 确保队列存在
channel.queue_declare(queue=queue_name, durable=True)


def callback(ch, method, properties, body):
    """
    消费者回调函数，处理接收到的消息，并将其输出。
    """
    try:
        # 将消息从二进制转成 JSON 并打印出来
        message = json.loads(body)
        print(f"收到消息：{message}")

        # 手动确认消息
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        print(f"消息不是有效的 JSON 格式：{body}")
        # 拒绝消息，避免重新入队（可选，视具体需求）
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


if __name__ == "__main__":
    # 消费消息
    channel.basic_qos(prefetch_count=1)  # 一次只获取一条消息
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print('等待接收消息，按 CTRL+C 退出')
    try:
        channel.start_consuming()  # 开始消费消息
    except KeyboardInterrupt:
        print('停止消费')
        channel.stop_consuming()

    # 关闭连接
    connection.close()