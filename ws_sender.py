import os
import websockets
import asyncio
import json


async def send_file(file_path, websocket):
    file_size = os.path.getsize(file_path)

    file_name = os.path.basename(file_path)  # 获取文件名
    chunk_size = 512 * 1024  # 每块大小为 512 KB

    # 发送文件传输元数据（包括文件名和文件大小）
    metadata = json.dumps({
        'file_name': file_name,
        'file_size': file_size
    })
    await websocket.send(metadata)

    # 等待接收端确认是否继续
    response = await websocket.recv()
    if response == 'ERROR: File exceeds size limit.':
        print("接收端拒绝接收文件，文件大小超过限制。")
        return

    # 分块发送文件数据
    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            await websocket.send(chunk)
            chunk = file.read(chunk_size)
        await websocket.send('EOF')  # 发送结束标志
    print(f"文件 {file_name} 已发送完成")


async def websocket_client(uri, file_path):
    async with websockets.connect(uri) as websocket:
        await send_file(file_path, websocket)


if __name__ == '__main__':
    file_path = 'sender/small.txt'  # 替换为你的文件路径
    asyncio.run(websocket_client('ws://localhost:9900', file_path))
