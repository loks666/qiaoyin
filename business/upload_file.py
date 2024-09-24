"""
import base64
import json
import websocket
import asyncio

# 图片文件路径
bg_image_path = 'path_to_your_image.jpg'
logo_image_path = 'path_to_your_image.jpg'

# 读取图片并转换为base64编码
with open(bg_image_path, 'rb') as bg_file:
    bgFile = base64.b64encode(bg_file.read()).decode('utf-8')

with open(logo_image_path, 'rb') as logo_file:
    logoFile = base64.b64encode(logo_file.read()).decode('utf-8')


# 创建要发送的数据
data = {
    'todo' : 'UPL_PNGFILE',
    'superID' : '10001',
    'systemID' : '101',

    'bfFileName' : bg_image_path,
    'bgFile' : bgFile,
    'bgMD5' : '',

    'logoFileName' : logo_image_path,
    'logoFile' : logoFile,
    'logoMD5' : '',
}

# WebSocket服务器的URL
ws_url = 'ws://your_websocket_server'

# 创建WebSocket连接
ws = websocket.create_connection(ws_url)
asyncio.get_event_loop().run_until_complete(send_image_over_websocket('ws://your_websocket_server'))

# 发送JSON数据
ws.send(json.dumps(data))

# 接收服务器响应（如果有的话）
response = ws.recv()

print("Received response:", response)

# 关闭WebSocket连接
ws.close()
"""


import asyncio
from http.client import responses

import websockets
import json
from io import BytesIO
from PIL import Image
from datetime import datetime
import hmac
import hashlib
import base64

def generate_hmac_sha_signature(message):
    cur = datetime.now()
    key = cur.strftime('%Y-%m-%d %H:%M:%S.%f')
    hmac_key = bytes(key, 'utf-8')
    hmac_message = bytes(message, 'utf-8')
    signature = hmac.new(hmac_key, hmac_message, hashlib.sha1).hexdigest()
    return signature

def gen_md5(file_name) :
    md5 = hashlib.md5()
    with open(file_name, 'rb') as f:
        # 一次读取并处理1024字节
        for chunk in iter(lambda: f.read(1024), b""):
            md5.update(chunk)
    return md5.hexdigest()

async def send_image_over_websocket(uri):
    async with websockets.connect(uri) as websocket:
        bg_image_path = 'bg.png'
        logo_image_path = 'lg.png'

        # 读取图片文件
        md5 = gen_md5(bg_image_path)
        image = Image.open(bg_image_path)
        byte_buffer = BytesIO()
        image.save(byte_buffer, format='PNG')
        byte_data = byte_buffer.getvalue()

        # 创建一个包含图片数据的JSON
        message_data = {
            'todo': 'UPL_PNGFILE',
            'superID': '10001',
            'systemID': '101',

            'bfFileName': bg_image_path,
            # 'bgFile': byte_data,
            'bgFile': '',
            'bgMD5': str(md5),

            'logoFileName': logo_image_path,
            'logoFile': '',
            'logoMD5': '',

            "needAnswer" : "yes"
            # 'image': byte_data,
            # 'message': 'Here is an image'
        }

        # if isinstance(message_data['bgFile'], bytes) :
        message_data['bgFile'] = base64.b64encode(byte_data).decode('utf8')

        md5 = gen_md5(logo_image_path)
        image = Image.open(logo_image_path)
        byte_buffer = BytesIO()
        image.save(byte_buffer, format='PNG')
        byte_data = byte_buffer.getvalue()

        message_data['logoFileName'] = logo_image_path
        message_data['logoFile'] = base64.b64encode(byte_data).decode('utf8')
        message_data['logoMD5'] = str(md5)
        # if isinstance(message_data['logoFile'], bytes):
        #     message_data['logoFile'] = base64.b64encode(byte_data).decode('utf8')

        # 序列化JSON
        json_message = json.dumps(message_data)

        # 发送JSON
        # await websocket.send(json_message)
        # response = await websocket.recv()
        # print(f"Received: {response}")

        # async with websockets.connect(uri) as websocket :
        #     await websocket.send(json_message)
        #     response = await websocket.recv()
        #     print(response)

        # chunk_size = 256 * 256
        # for i in range(0, len(json_message), chunk_size) :
        #     chunk = json_message[i : i + chunk_size]
        #     async with websockets.connect(uri) as websocket:
        #         await websocket.send(chunk)
        #         responses = await websocket.recv()
        #         print(responses)

        async with websockets.connect(uri) as websocket:
            chunk_size = 256 * 256
            l = len(json_message)
            for i in range(0, l, chunk_size) :
                chunk = json_message[i : i + chunk_size]
                await websocket.send(chunk)
            responses = await websocket.recv()
            print(responses)

if __name__ == "__main__" :
    uri = 'ws://60.204.169.49:9900'
    asyncio.run(send_image_over_websocket(uri))
# asyncio.get_event_loop().run_until_complete(send_image_over_websocket('ws://60.204.169.49:9900'))