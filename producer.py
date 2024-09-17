import asyncio
import json
import websockets
from websockets import WebSocketServerProtocol
from rabbit import produce  # 导入 produce 方法

# WebSocket 服务器地址和端口
WEBSOCKET_HOST = 'localhost'
WEBSOCKET_PORT = 9900

async def websocket_handler(websocket: WebSocketServerProtocol, path: str):
    """
    WebSocket 处理程序，接收设备发送的 JSON 数据，并将数据推送到 RabbitMQ。
    """
    print(f"设备已连接: {path}")
    try:
        async for message in websocket:
            try:
                # 假设设备发送的消息是 JSON 格式
                data = json.loads(message)
                print(f"接收到设备数据: {data}")
                # 将接收到的消息发送到 RabbitMQ
                produce(data)
            except json.JSONDecodeError:
                print(f"接收到的消息不是有效的 JSON: {message}")
    except websockets.ConnectionClosed:
        print("设备已断开连接")

async def start_websocket_server():
    """
    启动 WebSocket 服务器。
    """
    async with websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT):
        print(f"WebSocket 服务器已启动，等待设备连接... (ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT})")
        await asyncio.Future()  # 保持 WebSocket 服务器运行

if __name__ == "__main__":
    try:
        # 启动 WebSocket 服务器
        asyncio.get_event_loop().run_until_complete(start_websocket_server())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("服务器关闭中...")
