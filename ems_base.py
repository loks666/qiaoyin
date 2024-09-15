#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import threading
import hmac
import hashlib
import base64
from itertools import count

import pymysql

from datetime import datetime
from logging.handlers import RotatingFileHandler
from time import ctime, sleep

import pymysql
import datetime
import json
import logging
from dbutils.pooled_db import PooledDB, SharedDBConnection
from starlette.websockets import WebSocket

import socket

LOG_FORMAT = ("[%(asctime)s][ %(levelname)s ][pid: %(process)d][pname: %(processName)s][tid: %(thread)d]"
              "[tname: %(threadName)s][ %(name)s ][file: %(filename)s][func: %(funcName)s ]"
              "[line: %(lineno)d]: %(message)s")
rfh = logging.handlers.RotatingFileHandler(filename = 'ems_log.log', encoding = 'UTF-8', maxBytes = 10485760,
                                           backupCount = 100)
logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG, handlers = [rfh])

"""
logging.debug('this is print_hi debug')
logging.info('this is print_hi info')
logging.warning('this is print_hi warning')
logging.error('this is print_hi error')
logging.critical('this is print_hi critical')
"""

"""
db operation general
"""
ems_ds = {
    'host': '192.168.1.55',
    'port': 3306,
    'user': 'root',
    'password': 'joiningtek',
    'database': 'ems',
    'charset': 'utf8'
}

def conn_db():
    db_conn = pymysql.connect(**ems_ds)
    #db_conn = pymysql.connect(host=ems_ds['host'], port=ems_ds['port'], user=ems_ds['user'],
    #                       password=ems_ds['password'], charset=ems_ds['charset'], db=ems_ds['database'])
    db_cursor = db_conn.cursor()
    return db_conn, db_cursor

def close_db(*args):
    for item in args:
        item.close()

def db_exec(sql, **kwargs):
    db_cursor.execute(sql, kwargs)
    db_conn.commit()

def fetch_one(sql, **kwargs):
    db_cursor.execute(sql, kwargs)
    result = db_cursor.fetchone()
    return result

def fetch_all(sql, **kwargs):
    db_cursor.execute(sql, kwargs)
    result = db_cursor.fetchall()
    return result

db_conn, db_cursor = conn_db()

'''
if __name__ == '__main__':
    conn_db()
    sql = "select * from system_def"
    fetch_all(sql)
'''

"""
load network config from database, then identify system type is cloud or host, if host, is physical or virtual
"""
network = {
    'host_type': '',        # cloud, physic, virtual
    'local_ip': '',         # host or cloud ip
    'web_port': 0,         # host or cloud port to listen websocket communication
    'lora_port': 0,        # host or cloud port to listen lora MQTT communication
    'remote_port': 0,      # port, for host access cloud or cloud listen from host
    'net_mask': '',
    'local_gateway': '',

    'uplink_url': ''       # host access cloud url
}

web_conn = {
    'web_ip': '',
    'web_port': 0
}

lora_conn = {
    'lora_ip': '',
    'lora_port': 0
}

remote_conn = {
    'remote_ip': '',
    'remote_port': 0
}

class ems_db():
    __pool = None

    def __init__(self,
                 mincached=10,          # mincached:连接池中空闲连接的初始数量
                 maxcached=20,          # maxcached:连接池中空闲连接的最大数量
                 maxshared=10,          # maxshared:共享连接的最大数量
                 maxconnections=200,    # maxconnections:创建连接池的最大数量
                 blocking=True,         # blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
                 maxusage=100,          # maxusage:单个连接的最大重复使用次数
                 setsession=None,       # setsession:optional list of SQL commands that may serve to prepare the session,
                                        # e.g. ["set datestyle to ...", "set time zone ..."]
                 reset=True,            # reset:how connections should be reset when returned to the pool (False or
                                        # None to rollback transcations started with begin(), True to always issue a
                                        # rollback for safety's sake)
                 host=ems_ds['host'],       # host:数据库ip地址
                 port=ems_ds['port'],       # port:数据库端口
                 db=ems_ds['database'],     # db:库名
                 user=ems_ds['user'],       # user:用户名
                 passwd=ems_ds['password'],   # passwd:密码
                 charset=ems_ds['charset']  # charset:字符编码
                 ):

        if not self.__pool:
            self.__class__.__pool = PooledDB(pymysql,
                                             mincached, maxcached,
                                             maxshared, maxconnections, blocking,
                                             maxusage, setsession, reset,
                                             host=host, port=port, db=db,
                                             user=user, passwd=passwd,
                                             charset=charset,
                                             cursorclass=pymysql.cursors.DictCursor
                                             )
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            print(e)

    def __execute(self, sql, param=()):
        count = self._cursor.execute(sql, param)
        print(count)
        return count

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datatime对象转成字符串，使json转换不出错"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def select_one(self, sql, param=()):
        """查询单个结果"""
        count = self.__execute(sql, param)
        result = self._cursor.fetchone()
        """:type result:dict"""
        result = self.__dict_datetime_obj_to_str(result)
        return count, result

    def select_many(self, sql, param=()):
        """
        查询多个结果
        :param sql: qsl语句
        :param param: sql参数
        :return: 结果数量和查询结果集
        """
        count = self.__execute(sql, param)
        result = self._cursor.fetchall()
        """:type result:list"""
        [self.__dict_datetime_obj_to_str(row_dict) for row_dict in result]
        return count, result

    def execute(self, sql, param=()):
        count = self.__execute(sql, param)
        return count

    def begin(self):
        """开启事务"""
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """结束事务"""
        if option == 'commit':
            self._conn.autocommit()
        else:
            self._conn.rollback()

ems_db_conn = ems_db()

"""
if __name__ == "__main__":
    mc = MysqlClient()
    sql1 = 'SELECT * FROM shiji  WHERE  id = 1'
    result1 = mc.select_one(sql1)
    print(json.dumps(result1[1], ensure_ascii=False))

    sql2 = 'SELECT * FROM shiji  WHERE  id IN (%s,%s,%s)'
    param = (2, 3, 4)
    print(json.dumps(mc.select_many(sql2, param)[1], ensure_ascii=False))
"""


def get_network():
    sql = 'select * from network_conf'
    count, result = ems_db_conn.select_one(sql)

    system_type = result['system_type'].lower()
    host_type = result['host_type'].lower()
    if system_type == 'cloud' :
        network['host_type'] = 'cloud'
        network['local_ip'] = result['local_ip']
        network['web_port'] = result['web_port']
        network['lora_port'] = result['lora_port']
        network['remote_port'] = result['remote_port']

    elif system_type == 'host' and host_type == 'physic' :
        network['host_type'] = host_type
        network['local_ip'] = result['local_ip']
        network['web_port'] = result['web_port']
        network['lora_port'] = result['lora_port']
        network['remote_port'] = result['remote_port']
        network['net_mask'] = result['net_mask']
        network['local_gateway'] = result['local_gateway']
        network['uplink_url'] = result['uplink_url']

    elif system_type == 'host' and host_type == 'virtual' :
        network['host_type'] = host_type
        network['lora_port'] = result['lora_port']

    ems_ds['host'] = result['datasource_ip']
    ems_ds['port'] = result['datasource_port']
    ems_ds['user'] = result['datasource_usr']
    ems_ds['password'] = result['datasource_pwd']
    ems_ds['database'] = result['dataschema']
    ems_ds['charset'] = result['datacharset']

    logging.info('get_network interface: '  + str(network) + ' datasource: ' + str(ems_ds)  + ' sql:" ' + ' " ' + str(
        result))

get_network()

class ems_network() :
    def __init__(self, host_type, local_ip, web_port, lora_port, remote_port, net_mask, local_gateway, uplink_url):
        self.host_type = host_type
        self.local_ip = local_ip
        self.web_port = web_port
        self.lora_port = lora_port
        self.remote_port = remote_port
        self.net_mask = net_mask
        self.local_gateway = local_gateway
        self.uplink_url = uplink_url

    def websocket_connect(self):
        if self.host_type == 'cloud':
            web_conn.web_ip = self.local_ip
            web_conn.web_port = self.web_port
        elif self.host_type == 'physic':
            web_conn.web_ip = self.local_ip
            web_conn.web_port = self.web_port

    def lora_connect(self):
        if self.host_type == 'cloud':
            lora_conn.lora_ip = self.local_ip
            lora_conn.lora_port = self.lora_port
        elif self.host_type == 'physic':
            lora_conn.lora_ip = self.local_ip
            lora_conn.lora_port = self.lora_port

    def remote_connect(self):
        if self.host_type == 'cloud':
            remote_conn.lora_ip = self.local_ip
            remote_conn.lora_port = self.remote_port
        elif self.host_type == 'physic':
            remote_conn.lora_ip = socket.gethostbyname(self.uplink_url)
            remote_conn.lora_port = self.remote_port



"""
initiate thread and start
"""
class MyThread(threading.Thread):
    def __init__(self, func, args, name='', daemon=True):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.daemon = daemon

    def getResult(self):
        return self.res

    def run(self):
        # print('[ ', ctime(), ' ] Thread: ', self.name, ' is now booting !', )
        logging.info(self.name + ' is running')
        self.res = self.func(*self.args)
        # self.func(*self.args)

# generate token and md5
def encode_to_base64(input_string):
    # 将字符串编码为字节
    byte_string = input_string.encode('utf-8')

    # 使用base64编码
    base64_bytes = base64.b64encode(byte_string)

    # 将编码结果转换为字符串
    base64_string = base64_bytes.decode('utf-8')

    return base64_string



"""
original_string = "Hello, World!"
encoded_string = encode_to_base64(original_string)
print(f"原始字符串: {original_string}")
print(f"Base64编码: {encoded_string}")
"""

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

def gen_md5(file_name) :
    md5 = hashlib.md5()
    with open(file_name, 'rb') as f:
        # 一次读取并处理1024字节
        for chunk in iter(lambda: f.read(1024), b""):
            md5.update(chunk)
    return md5.hexdigest()


"""
Buffer, from receipt to sync, definition
"""
class ems_buf ():
    ems_buf = {
        'web': [],
        'lora': [],
        'host': []
    }
    def __init__(self, name='', seq_no=''):
        self.name = name
        self.seq_no = seq_no

    def append(self, name, seq_no):
        self.ems_buf[name].append(seq_no)

    def delete(self, name, seq_no):
        self.ems_buf[name].remove(seq_no)

ems_recv = ems_buf()







