# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from web_socket import start
import asyncio
import logging
from logging.handlers import RotatingFileHandler

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


LOG_FORMAT = ("[%(asctime)s][ %(levelname)s ][pid: %(process)d][pname: %(processName)s][tid: %(thread)d]"
              "[tname: %(threadName)s][ %(name)s ][file: %(filename)s][func: %(funcName)s ]"
              "[line: %(lineno)d]: %(message)s")
# rfh = logging.handlers.RotatingFileHandler(filename = 'ems_log.log', encoding = 'UTF-8', maxBytes = 10485760,
#                                            backupCount = 100)
# logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG, handlers = [rfh])

"""
logging.debug('this is print_hi debug')
logging.info('this is print_hi info')
logging.warning('this is print_hi warning')
logging.error('this is print_hi error')
logging.critical('this is print_hi critical')
"""

"""
def find_obj(json_obj, key):
    try:
        if isinstance(json_obj, dict):
            if key in json_obj:
                return find_obj[key]
            else:
                for sub_obj in json_obj.values():
                    result = find_obj(sub_obj, key)
                    if result:
                        return result
        elif isinstance(json_obj, list):
            for sub_obj in json_obj:
                result = find_obj(sub_obj, key)
                if result:
                    return result
    except (KeyError, TypeError):
        pass
    return None

def encode_to_base64(input_string):
    # 将字符串编码为字节
    byte_string = input_string.encode('utf-8')

    # 使用base64编码
    base64_bytes = base64.b64encode(byte_string)

    # 将编码结果转换为字符串
    base64_string = base64_bytes.decode('utf-8')

    return base64_string

def generate_hmac_sha_signature(message):
    cur = datetime.now()
    key = cur.strftime('%Y-%m-%d %H:%M:%S.%f')
    hmac_key = bytes(key, 'utf-8')
    hmac_message = bytes(message, 'utf-8')
    signature = hmac.new(hmac_key, hmac_message, hashlib.sha1).hexdigest()
    return signature

def gen_token(phone_num, user_name) :
    message = "1" + phone_num + user_name
    # print(message)
    signature = generate_hmac_sha_signature(message)
    # print("HMAC SHA256 签名：", signature)
    return (encode_to_base64(signature))

# def gen_md5(file_name) :
#     md5 = hashlib.md5()
#     with open(file_name, 'rb') as f:
#         # 一次读取并处理1024字节
#         for chunk in iter(lambda: f.read(1024), b""):
#             md5.update(chunk)
#     return md5.hexdigest()
"""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rfh = logging.handlers.RotatingFileHandler(filename='/home/raymond/project/test/api_log.log', encoding='UTF-8',
                                               maxBytes=10485760,
                                               backupCount=100)
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, handlers=[rfh])
    logging.critical('\n\n\tapt test is now booting ......\n')
    asyncio.run(start())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
