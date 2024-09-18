# consumer.py

import time
import threading
import queue
from rabbit import consume  # 导入 consume 方法
import websocket
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket 服务器地址
WS_SERVER_URI = 'ws://localhost:8765'  # 替换为你的 WebSocket 服务器地址

# 创建一个线程安全的队列，用于发送消息
message_queue = queue.Queue()

class WebSocketClient(threading.Thread):
    def __init__(self, uri, message_queue):
        super().__init__()
        self.uri = uri
        self.message_queue = message_queue
        self.ws = None
        self.running = True

    def on_open(self, ws):
        logger.info("WebSocket 连接已打开")

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(f"WebSocket 连接已关闭: {close_status_code} - {close_msg}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket 连接出错: {error}")

    def run(self):
        while self.running:
            try:
                self.ws = websocket.WebSocketApp(
                    self.uri,
                    on_open=self.on_open,
                    on_close=self.on_close,
                    on_error=self.on_error
                )
                self.ws.run_forever(ping_interval=60)
            except Exception as e:
                logger.error(f"WebSocket 运行时出错: {e}")
                time.sleep(5)  # 等待一段时间后重试

    def send_message(self, message):
        """
        发送消息到 WebSocket 服务器。
        """
        if self.ws and self.ws.sock and self.ws.sock.connected:
            try:
                self.ws.send(json.dumps(message))
                logger.info(f"已通过 WebSocket 发送消息：{message}")
            except Exception as e:
                logger.error(f"通过 WebSocket 发送消息时出错：{e}")
        else:
            logger.warning("WebSocket 尚未连接，无法发送消息")

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()

def websocket_sender(ws_client, message_queue):
    """
    线程函数，从队列中获取消息并通过 WebSocket 发送。
    """
    while True:
        try:
            message = message_queue.get()
            if message is None:
                break
            ws_client.send_message(message)
        except Exception as e:
            logger.error(f"发送消息时出错：{e}")

def process_message(message):
    """
    处理消费到的消息，例如通过 WebSocket 发送到其他服务。
    """
    # 示例：打印消息
    logger.info(f"处理消息：{message}")
    # 将消息放入队列以通过 WebSocket 发送
    message_queue.put(message)

if __name__ == "__main__":
    # 启动 WebSocket 客户端线程
    ws_client = WebSocketClient(WS_SERVER_URI, message_queue)
    ws_client.start()
    logger.info("WebSocket 客户端已启动")

    # 启动发送线程
    sender_thread = threading.Thread(target=websocket_sender, args=(ws_client, message_queue))
    sender_thread.start()
    logger.info("WebSocket 发送线程已启动")

    try:
        while True:
            message = consume()
            if message:
                process_message(message)
            else:
                # 如果没有消息，等待一段时间后再尝试
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("消费者停止运行")
    finally:
        # 停止 WebSocket 客户端和发送线程
        message_queue.put(None)  # 发送终止信号
        sender_thread.join()
        ws_client.stop()
        ws_client.join()
        logger.info("WebSocket 客户端已关闭")
