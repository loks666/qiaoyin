import time
from rabbit import consume  # 导入 consume 方法

def process_message(message):
    """
    处理消费到的消息，例如发送到其他 API 或网站。
    """
    # 示例：打印消息
    print(f"处理消息：{message}")
    # 这里可以添加发送到其他 API 的逻辑
    # 例如：
    import requests
    response = requests.post('https://example.com/api/data', json=message)
    if response.status_code == 200:
        print("成功发送到 API")
    else:
        print("发送到 API 失败")

if __name__ == "__main__":
    print("开始消费 RabbitMQ 中的消息...")
    try:
        while True:
            message = consume()
            if message:
                process_message(message)
            else:
                # 如果没有消息，等待一段时间后再尝试
                time.sleep(1)
    except KeyboardInterrupt:
        print("消费者停止运行")
