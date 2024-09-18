import asyncio
import json
import websockets
from websockets import WebSocketServerProtocol
from rabbit import produce  # 导入 produce 方法

# WebSocket 服务器地址和端口
WEBSOCKET_HOST = 'localhost'
WEBSOCKET_PORT = 9900

# 全局连接池，存储连接序号和对应的 websocket 对象
connected_clients = {}
# 全局序号计数器
client_counter = 0

async def websocket_handler(websocket: WebSocketServerProtocol, path: str):
    """
    WebSocket 处理程序，接收设备发送的 JSON 数据，并将数据推送到 RabbitMQ。
    同时，将每个连接按照顺序编号保存到连接池。
    """
    global client_counter
    # 分配序号
    client_id = client_counter
    client_counter += 1

    # 将连接保存到连接池
    connected_clients[client_id] = websocket
    print(f"设备已连接: {path}，分配的序号为 {client_id}")

    try:
        async for message in websocket:
            try:
                # 假设设备发送的消息是 JSON 格式
                data = json.loads(message)
                print(f"接收到设备 {client_id} 的数据: {data}")
                # 将接收到的消息发送到 RabbitMQ
                produce(data)
            except json.JSONDecodeError:
                print(f"接收到的消息不是有效的 JSON: {message}")
    except websockets.ConnectionClosed:
        print(f"设备 {client_id} 已断开连接")
    finally:
        # 从连接池中移除断开的连接
        del connected_clients[client_id]
        print(f"已从连接池中移除设备 {client_id}")

async def start_websocket_server():
    """
    启动 WebSocket 服务器。
    """
    async with websockets.serve(websocket_handler, WEBSOCKET_HOST, WEBSOCKET_PORT):
        print(f"WebSocket 服务器已启动，等待设备连接... (ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT})")
        await asyncio.Future()  # 保持 WebSocket 服务器运行

async def send_message_to_client(client_id, message):
    """
    发送消息给指定的客户端。
    :param client_id: 客户端的序号
    :param message: 要发送的消息（字符串或 JSON 格式）
    """
    websocket = connected_clients.get(client_id)
    if websocket:
        try:
            await websocket.send(json.dumps(message))
            print(f"已向客户端 {client_id} 发送消息：{message}")
        except Exception as e:
            print(f"发送消息给客户端 {client_id} 时出错：{e}")
    else:
        print(f"客户端 {client_id} 未连接")


if __name__ == "__main__":
    try:
        # 启动 WebSocket 服务器
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        print("服务器关闭中...")
    # 示例：假设您想向序号为 2 的客户端发送消息
    message = {"type": "notification", "content": "这是给您的消息"}
    send_message_to_client(2, message)


