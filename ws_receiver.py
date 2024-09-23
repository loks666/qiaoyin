import asyncio
import json
import websockets
import os

# 文件大小限制（单位：字节）
FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5MB

async def websocket_handler(websocket, path):
    while True:
        try:
            # 接收文件元数据
            metadata = await websocket.recv()
            try:
                metadata = json.loads(metadata)
                file_name = metadata.get('file_name')
                file_size = metadata.get('file_size')

                # 检查文件名和文件大小是否存在
                if not file_name or not file_size:
                    raise ValueError("缺少文件名或文件大小")

                print(f"接收到的文件名: {file_name}, 文件大小: {file_size} 字节")

                # 判断文件大小是否超过限制
                if file_size > FILE_SIZE_LIMIT:
                    await websocket.send('ERROR: File exceeds size limit.')
                    print(f"文件 {file_name} 大小超过限制，不接受该文件。")
                    continue
                else:
                    await websocket.send('OK')  # 继续传输文件

            except (json.JSONDecodeError, ValueError) as e:
                # 如果元数据解析失败或缺少字段，拒绝文件传输
                await websocket.send('ERROR: Invalid file metadata.')
                print(f"文件元数据无效: {e}")
                continue

            file_data = b''  # 用于存储文件的字节数据

            try:
                while True:
                    # 接收文件分块数据
                    data = await websocket.recv()

                    if isinstance(data, str) and data == 'EOF':
                        print("文件接收完成，收到 EOF")
                        break  # 接收完成

                    if isinstance(data, bytes):
                        file_data += data  # 合并文件块

                # 创建receiver目录（如果不存在）
                save_dir = os.path.join(os.getcwd(), 'receiver')
                os.makedirs(save_dir, exist_ok=True)

                # 保存接收到的文件到receiver目录
                file_path = os.path.join(save_dir, file_name)
                with open(file_path, 'wb') as file:
                    file.write(file_data)
                print(f'文件 {file_name} 已成功保存到 {file_path}')

            except Exception as e:
                print(f"文件传输错误: {e}")

            finally:
                print(f"清理资源，关闭文件传输请求: {file_name}")

        except websockets.ConnectionClosed:
            print("连接已关闭")
            break

async def start_server():
    port = 9900
    print("\nwebsocket server 启动：ws://127.0.0.1:" + str(port))
    server = await websockets.serve(websocket_handler, '0.0.0.0', port)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(start_server())
