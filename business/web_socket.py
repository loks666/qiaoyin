#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
from idlelib.outwin import OnDemandOutputWindow
from tkinter import image_types

import websockets
import json
from datetime import datetime
import ems_verify_sms as sms
import logging
import hashlib
import base64
import hmac
# from PIL import Image
# from io import BytesIO

# import chardet
# from main import LOG_FORMAT

reply = {}
allen = 'Allen'
jn = '上海桥茵自动化设备有限公司'

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

def gen_md5(file_name) :
    md5 = hashlib.md5()
    with open(file_name, 'rb') as f:
        # 一次读取并处理1024字节
        for chunk in iter(lambda: f.read(1024), b""):
            md5.update(chunk)
    return md5.hexdigest()


def write_data_file(data, file_name, md5):
    ret = {
        'code' : False,
        'bytes' : 0,
        'md5' : ''
    }
    if data:
        data_bytes = base64.b64decode(data)
        with open(file_name, 'wb') as f:
            f.write(data_bytes)
            f.close()
            ret['bytes'] = len(data_bytes)
            ret['md5'] = gen_md5(file_name)
            if ret['md5'] == md5:
                ret['code'] = True

    return ret

def get_whether():
    return temp, humi




#async def websocket(accept):
async def websocket(accept, path):
       async for recv_data in accept:
        """
        recv_data = await accept.recv()
        # print(recv_data)
        logging.info('\n' + str(recv_data))
        """
        # 假设接收到的数据是 JSON 格式的字符串
        try:
            # 将 bytes 解码为字符串，然后解析 JSON 数据
            data = json.loads(recv_data)

            if isinstance(data['bgFile'], bytes):
                image_base64 = data['bgFile']
                image_data = base64.b64decode(image_base64)
                with open(path, 'wb') as f:
                    f.write(image_data)
                    f.close()
                    data['bgFile'] = ''

            if isinstance(data['logoFile'], bytes):
                image_base64 = data['logoFile']
                image_data = base64.b64decode(image_base64)
                with open(path, 'wb') as f:
                    f.write(image_data)
                    f.close()
                    data['logoFile'] = ''

            logging.info('\n' + str(data))
            logging.info('\n' + str(recv_data))

            # 比较字典中的 'todo' 键的值
            if data['todo'] == 'GET_SUPERVERIFY':       # 1.1.1
                code = sms.gen_verify_code()
                reply = sms.send_verify_code('18621326705', code)
                logging.info('send sms: ' + str(reply))
                # print(reply)
                reply = {
                    'what' : 'GET_SUPERVERIFY',
                    'code' : 'OK'
                }
            elif data['todo'] == 'SET_SUPERLOGIN':      # 1.1.2
                if data['superName'] == allen :
                    reply = {
                        'what' : 'SET_SUPERLOGIN',
                        'code' : '0',
                        'superID' : '10001'
                    }
                else :
                    reply = {
                        'what' : 'SET_SUPERLOGIN',
                        'code' : '3',
                        'errNo' : '3',
                        'errMsg' : '账号密码验证码错误'
                    }
            elif data['todo'] == 'QRY_SYSNAME':         # 1.2.1
                if data['adminName'] == allen :
                    reply = {
                        'what' : 'QRY_SYSNAME',
                        'code' : '3',
                        'errNo' : '2',
                        'errMsg' :  '此注册名已被用'
                    }
                elif data['corpName'] == jn :
                    reply = {
                        'what' : 'QRY_SYSNAME',
                        'code' : '3',
                        'errNo' : '4',
                        'errMsg' : '此单位名已被用'
                    }
                else :
                    reply = {
                        'what' : 'QRY_SYSNAME',
                        'code' : '0',
                        'systemID' : '101',
                        'adminID' : '20001'
                    }
            elif data['todo'] == 'GET_ADMINVERIFY':     # 1.2.2
                code = sms.gen_verify_code()
                phone = data['adminPhone']
                reply = sms.send_verify_code(phone, code)
                # print(reply)
                logging.info('send sms: ' + str(reply))
                reply = {
                    'what' : 'GET_ADMINVERIFY',
                    'code' : 'OK'
                }
            elif data['todo'] == 'ADD_NEWSYSTEM':       # 1.2.3
                dt = datetime.now()
                if data['superID'] == '10001' :
                    reply = {
                        'what' : 'ADD_NEWSYSTEM',
                        'code' : '0',
                        'setupTime' : str(dt)
                    }
                else :
                    reply = {
                        'what' : 'ADD_NEWSYSTEM',
                        'code' : '3',
                        'errNo' : '1',
                        'errMsg' : '操作失败'
                    }
            elif data['todo'] == 'MDF_CURSYSTEM':       # 1.2.4
                dt = datetime.now()
                if data['systemID'] == '101' :
                    reply = {
                        'what': 'MDF_CURSYSTEM',
                        'code': '3',
                        'errNo': '1',
                        'errMsg': '操作失败'
                    }
                else :
                    reply = {
                        'what': 'MDF_CURSYSTEM',
                        'code': '0',
                        'setupTime': str(dt)
                    }

            elif data['todo'] == 'UPL_PNGFILE':         # 1.2.5
                reply = {
                    'what': 'UPL_PNGFILE',
                    'code': '',
                    'errNo': '',
                    'errMsg': ''
                }
                phone_num = '13701842571'               # get from database
                if len(data['bgFileName']) > 0 :
                    file_name = gen_md5(phone_num, data['pngFileName'])
                    ret = write_data_file(data['pngFile'], file_name, data['pngMD5'])
                    if ret['code'] == False:
                        reply = {
                            'what' : 'UPL_PNGFILE',
                            'code' : '3',
                            'errNo' : '8',
                            'errMsg' : data['pngFileName'] + ' ' + '上传文件失败'
                        }
                    else :
                        reply = {
                            'what' : 'UPL_PNGFILE',
                            'code' : '0',
                            'pngToken' : file_name
                        }

                if len(data['logoFileName']) > 0 :
                    file_name = gen_md5(phone_num, data['logoFileName'])
                    ret = write_data_file(data['logoFile'], file_name, data['logoMD5'])
                    if ret['code'] == False:
                        reply['code'] = '3'
                        reply['errNo'] = '8'
                        reply['errMsg'] += ' ' + data['logoFileName'] + ' ' + '上传文件失败'
                    else :
                        reply['logoToken'] = file_name

            elif data['todo'] == 'DIS_ENABLE':         # 1.2.6
                dt = datetime.now()
                if data['manage'] == 'ENABLE' :
                    reply = {
                        'what' : 'DIS_ENABLE',
                        'code' : '0',
                        'setupTime' : str(dt)
                    }
                else :
                    reply = {
                        'what' : 'DIS_ENABLE',
                        'code' : '3',
                        'errNo' : '1',
                        'errMsg' : '操作失败'
                    }
            elif data['todo'] == 'QRY_SYSTEMLIST':      # 1.2.7
                if data['superID'] == '10001' :
                    reply = {
                        'what' : 'QRY_SYSTEMLIST',
                        'code' : '0',
                        'number' : '2',
                        'system' : [
                            {
                                'systemID': '10001',
                                'dispSystem': '上海桥茵科技智慧能率管理系统',
                                'corpName': '上海桥茵自动化设备有限公司',
                                'adminID': '20001',
                                'adminName': 'Allen',
                                'adminPhoneNum': '12345678901',
                                'status': 'ENABLE',
                                'setupTime': '2024-08-21 10:20:20'
                            },
                            {
                                'systemID': '10002',
                                'dispSystem': '北京桥茵科技智慧能率管理系统',
                                'corpName': '北京桥茵自动化设备有限公司',
                                'adminID': '20002',
                                'adminName': 'Raymond',
                                'adminPhoneNum': '92345678901',
                                'status': 'DISABLE',
                                'setupTime': '2022-07-21 10:20:20'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'QRY_SYSTEMLIST',
                        'code' : '3',
                        'number' : '1',
                        'errMsg' : '操作失败'
                    }
            elif data['todo'] == 'QRY_USERNAME':         # 2.1.1
                if data['userName'] == allen:
                    reply = {
                        'what' : 'QRY_USERNAME',
                        'code' : '0',
                        'userID' : '20002'
                    }
                else :
                    reply = {
                        'what' : 'QRY_USERNAME',
                        'code' : '3',
                        'errNo' : '4',
                        'errMsg': '此注册名已被用'
                    }
            elif data['todo'] == 'GET_REGVRIFY':         # 2.1.2
                if len(data['userPhone']) >= 11:
                    code = sms.gen_verify_code()
                    reply = sms.send_verify_code(str(data['userPhone']), code)
                    logging.info('send sms: ' + str(reply))
                    reply = {
                        'what' : 'GET_REGVRIFY',
                        'code' : 'OK'
                    }
            elif data['todo'] == 'SET_REGISTER':         # 2.1.3
                if data['verifyCode'] == '000000' :
                    token = gen_token(str(data['userPhone']), str(data['userName']))
                    reply = {
                        'what' : 'SET_REGISTER',
                        'code' : '0',
                        'token' : str(token)
                    }
                else :
                    reply = {
                        'what' : 'SET_REGISTER',
                        'code' : '3',
                        'errNo' : '5',
                        'errMsg' : '注册失败，请联系客服'
                    }
            elif data['todo'] == 'GET_LOGVERIFY':         # 2.2.1
                if data['userName'] == allen:
                    code = sms.gen_verify_code()
                    reply = sms.send_verify_code('18621326705', code)
                    # reply = sms.send_verify_code('13701842571', code)
                    logging.info('send sms: ' + str(reply))
                    reply = {
                        'what' : 'GET_REGVRIFY',
                        'code' : 'OK'
                    }
            elif data['todo'] == 'SET_LOGINWITHUNAME':      # 2.2.2
                if data['userName'] == allen:
                    reply = {
                        'what' : 'SET_LOGINWITHUNAME',
                        'code' : '0',
                        'userID' : '20001',
                        'token' : 'abcde12345'
                    }
                else :
                    reply = {
                        'what' : 'SET_LOGINWITHUNAME',
                        'code' : '3',
                        'errNo' : '6',
                        'errMsg' : '登录失败，请联系客服'
                    }
            elif data['todo'] == 'SET_LOGINWITHTOEKN':         # 2.3.1
                if data['userID'] != '200001':
                    reply = {
                        'what' : 'SET_LOGINWITHUNAME',
                        'code' : '0',
                        'token' : 'abcde12345'
                    }
                else :
                    reply = {
                        'what' : 'SET_LOGINWITHUNAME',
                        'code' : '3',
                        'errNo' : '6',
                        'errMsg' : '登录失败，请联系客服'
                    }
            elif data['todo'] == 'SET_HEARTBEAT':           # 2.4.1
                logging.info('heartbeat from systemID:%s userID:%s' % (str(data['systemID']), str(data['userID'])))
                reply = {}
            elif data['todo'] == 'SET_LOGOUT':               # 2.5.1
                logging.info('logout from systemID:%s userID:%s' % (str(data['systemID']), str(data['userID'])))
                reply = {}
                # close websocket
                # ws_client.stop()
                # ws_client.join()
            elif data['todo'] == 'QRY_AREA':                # 3.1.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'QRY_AREA',
                        'code' : '0',
                        'first' : '1',
                        'number' : '3',
                        'area' : [
                            {
                                'areaID' : '1',
                                'areaNo' : '10101',
                                'areaName' : '一号楼101室',
                                'areaLocation' : 'B1 L1 R1',
                                'areaValue' : '50.5',
                                'areaHeight' : '2.9',
                                'memo' : '综合教学空间'
                            },
                            {
                                'areaID': '2',
                                'areaNo': '10201',
                                'areaName': '一号楼201室',
                                'areaLocation': 'B1 L2 R1',
                                'areaValue': '100.5',
                                'areaHeight': '2.9',
                                'memo': '综合教学空间'
                            },
                            {
                                'areaID': '5',
                                'areaNo': '20101',
                                'areaName': '二号楼101室',
                                'areaLocation': 'B2 L1 R1',
                                'areaValue': '200.5',
                                'areaHeight': '3.6',
                                'memo': '综合体育教学空间'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'QRY_AREA',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg' : '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'ADD_AREA':                # 3.1.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'ADD_AREA',
                        'code' : '0',
                        'number' :  '2',
                        'area' : [
                            {
                                'areaID' : '1',
                                'areaNo' : '10101',
                            },
                            {
                                'areaID': '5',
                                'areaNo': '20101',
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'ADD_AREA',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg' : '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'MDF_AREA':                # 3.1.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'MDF_AREA',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'MDF_AREA',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'DEL_AREA':                # 3.1.4
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'DEL_AREA',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'DEL_AREA',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'ADD_HOST':                # 4.1.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'ADD_HOST',
                        'code' : '0',
                        'hostID' : '20001',
                        'devEUI' : '4022d8fffe5e101b',
                        'maxConnection' : '500',
                        'location' : '上海市闵行区向阳路莲花路歆翱智联大厦',
                        'latitude' : '20.219035 E',
                        'logotude' : '32.678291 N'
                    }
                else :
                    reply = {
                        'what' : 'ADD_HOST',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'MDF_HOST':                # 4.1.2
                if data['systemID'] == '101':
                    reply = {
                        'what': 'MDF_HOST',
                        'code': '0',
                        'hostID': '20001',
                        'devEUI': '4022d8fffe5e1fff',
                        'maxConnection': '500',
                        'location': '上海市闵行区向阳路莲花路歆翱智联大厦',
                        'latitude': '20.219035 E',
                        'logotude': '32.678291 N'
                    }
                else:
                    reply = {
                        'what': 'MDF_HOST',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'DEL_HOST':                # 4.1.3
                if data['systemID'] == '101':
                    reply = {
                        'what': 'DEL_HOST',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what': 'DEL_HOST',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_HOST':                # 4.1.4
                if data['number'] > str(0):
                    reply = {
                        'what' : 'QRY_HOST',
                        'code' : '0',
                        'first' : '1',
                        'number' : '2',
                        'host' : [
                            {
                                'hostID' : '20001',
                                'hostNo' : '20001',
                                'devEUI' : '4022d8fffe5e1fff',
                                'hostName' : '能耗管理系统主机1号',
                                'hostType' : 'SERVER',
                                'maxConnection' : '500',
                                'memo' : '能耗管理系统主机1号'
                            },
                            {
                                'hostID': '20002',
                                'hostNo': '20002',
                                'devEUI': '4552d8fffe5e1fff',
                                'hostName': '能耗管理系统主机1号',
                                'hostType': 'SERVER',
                                'maxConnection': '500',
                                'memo': '能耗管理系统主机1号'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'QRY_HOST',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'ADD_NODE':                # 4.2.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'ADD_NODE',
                        'code' : '0',
                        'number' : '5',
                        'node' : [
                            {
                                'nodeID' : '50001',
                                'devEUI' : '4022d8fffe5e1fff'
                            },
                            {
                                'nodeID': '50002',
                                'devEUI': '4022f8fffe5e1fff'
                            },
                            {
                                'nodeID': '50003',
                                'devEUI': '4042d8fffe5e1fff'
                            },
                            {
                                'nodeID': '50001',
                                'devEUI': '4022dafffe5e1fff'
                            },
                            {
                                'nodeID': '50005',
                                'devEUI': '402dd8fffe5e1fff'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'ADD_NODE',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'MDF_NODE':                # 4.2.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'MDF_NODE',
                        'code' : '0',
                        'number' : '5',
                        'node' : [
                            {
                                'nodeID' : '50001',
                                'devEUI' : '4022d8fffe5e1fff'
                            },
                            {
                                'nodeID': '50002',
                                'devEUI': '4022f8fffe5e1fff'
                            },
                            {
                                'nodeID': '50003',
                                'devEUI': '4042d8fffe5e1fff'
                            },
                            {
                                'nodeID': '50001',
                                'devEUI': '4022dafffe5e1fff'
                            },
                            {
                                'nodeID': '50005',
                                'devEUI': '402dd8fffe5e1fff'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'MDF_NODE',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'DEL_NODE':                # 4.2.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'DEL_NODE',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'DEL_NODE',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_NODE':                # 4.2.4
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'QRY_NODE',
                        'code' : '0',
                        'first' : '1',
                        'number' : '3',
                        'node' : [
                            {
                                'nodeID' : '50001',
                                'nodeNo' : '2-2-1',
                                'devEUI' : '4022d8fffe5e1fff',
                                'nodeName' : '一零一空调',
                                'nodeType' : '空调执行器',
                                'nodePort' : '1',
                                'memo' : '101室指令热空调。。。。'
                            },
                            {
                                'nodeID': '50011',
                                'nodeNo': '2-2-1',
                                'devEUI': '402ad8fffe5e1fff',
                                'nodeName': '一零一开关',
                                'nodeType': '空调执行器',
                                'nodePort': '1',
                                'memo': '101室指令热空调。。。。'
                            },
                            {
                                'nodeID': '50031',
                                'nodeNo': '2-2-4',
                                'devEUI': '4022f8fffe5e1fff',
                                'nodeName': '一零一空调',
                                'nodeType': '空调执行器',
                                'nodePort': '1',
                                'memo': '101室指令热空调。。。。'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'QRY_NODE',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'ADD_EQUIP':               # 4.3.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'ADD_EQUIP',
                        'code' : '0',
                        'number' : '3',
                        'equip' : [
                            {
                                'equipID': '30301',
                                'equipNo': '3-2-001'
                            },
                            {
                                'equipID': '33301',
                                'equipNo': '3-3-001'
                            },
                            {
                                'equipID': '34301',
                                'equipNo': '3-4-001'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'ADD_EQUIP',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'MDF_EQUIP':               # 4.3.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'MDF_EQUIP',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'MDF_EQUIP',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'DEL_EQUIP':               # 4.3.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'DEL_EQUIP',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'DEL_EQUIP',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_EQUIP':               # 4.3.4
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'QRY_EQUIP',
                        'code' : '0',
                        'first' : '1',
                        'number' : '3',
                        'equip' : [
                            {
                                'equipID': '30301',
                                'equipNo': '3-2-001',
                                'equipName' : '教务处空调',
                                'portNo' : '1',
                                'areaID' : '201023',
                                'memo' : '教务处空调'
                            },
                            {
                                'equipID': '30305',
                                'equipNo': '3-2-201',
                                'equipName': '教务处空调',
                                'portNo': '1',
                                'areaID': '2-1-201023',
                                'memo' : '教务处空调'
                            },
                            {
                                'equipID': '30321',
                                'equipNo': '3-2-001',
                                'equipName': '教务处空调',
                                'portNo': '1',
                                'areaID': '2-1-201023',
                                'memo' : '教务处空调'
                            }
                        ]
                    }
                else:
                    reply = {
                        'what': 'QRY_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'ADD_TASK':               # 5.1.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'ADD_TASK',
                        'code' : '0',
                        'taskID' : '301',
                        'taskNo' : 'M-F-1-2',
                    }
                else :
                    reply = {
                        'what' : 'ADD_TASK',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'MDF_TASK':                # 5.1.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'MDF_TASK',
                        'code' : '0',
                        'taskID': '301',
                        'taskNo': 'S-F-1-2',
                    }
                else :
                    reply = {
                        'what' : 'MDF_TASK',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'DEL_TASK':                # 5.1.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'DEL_TASK',
                        'code' : 'OK'
                    }
                else :
                    reply = {
                        'what' : 'DEL_TASK',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_TASK':                # 5.1.4
                if data['systemID'] == '101':
                    dt = datetime.today()
                    reply = {
                        'what' : 'QRY_TASK',
                        'code' : '0',
                        'number' : '2',
                        'task' : [
                            {
                                'taskID' : '301',
                                'taskNo' : 'S-F-1-2',
                                'tackName' : '周一至周五教学空调计划',
                                'taskType' : 'TIMING',
                                'cycleNum' : '1',
                                'action' : 'TURN-ON',
                                'actOnTime' : '720',        # 分钟
                                'setupDay' : str(dt),
                                'repeatMode' : 'WORKDAY',
                                'intervalDay' : '',
                                'actDay' : '',
                                'number1' : '1',
                                'start' : [
                                    {
                                        'startTime' : '8:00:00',
                                    }
                                ],
                                'number2' : '0',
                                'number3' : '10',
                                'equip' : [
                                    {
                                        'equipID' : '30301'
                                    },
                                    {
                                        'equipID': '30302'
                                    },
                                    {
                                        'equipID': '30303'
                                    },
                                    {
                                        'equipID': '30304'
                                    },
                                    {
                                        'equipID': '30305'
                                    },
                                    {
                                        'equipID': '30306'
                                    },
                                    {
                                        'equipID': '30307'
                                    },
                                    {
                                        'equipID': '30308'
                                    },
                                    {
                                        'equipID': '30309'
                                    },
                                    {
                                        'equipID': '30311'
                                    }
                                ],
                                'concurrent' : '10',
                                'memo' : '教育楼空调计划'
                            },
                            {
                                'taskID': '302',
                                'taskNo': 'S-S-1-2',
                                'tackName': '周一至周五教学空调计划',
                                'taskType': 'TIMING',
                                'cycleNum': '1',
                                'action': 'TURN-ON',
                                'actOnTime': '820',  # 分钟
                                'setupDay': str(dt),
                                'repeatMode': 'WORKDAY',
                                'intervalDay': '',
                                'actDay': '',
                                'number1': '1',
                                'start': [
                                    {
                                        'startTime': '7:00:00',
                                    }
                                ],
                                'number2': '0',
                                'number3': '10',
                                'equip': [
                                    {
                                        'equipID': '30311'
                                    },
                                    {
                                        'equipID': '30312'
                                    },
                                    {
                                        'equipID': '30313'
                                    },
                                    {
                                        'equipID': '30314'
                                    },
                                    {
                                        'equipID': '30315'
                                    },
                                    {
                                        'equipID': '30316'
                                    },
                                    {
                                        'equipID': '30317'
                                    },
                                    {
                                        'equipID': '30318'
                                    },
                                    {
                                        'equipID': '30319'
                                    },
                                    {
                                        'equipID': '30321'
                                    }
                                ],
                                'concurrent': '10',
                                'memo': '教育楼空调计划'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'QRY_TASK',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'SET_TASKMODE':             # 6.1.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'SET_TASKMODE',
                        'code' : '0',
                        'taskID' : '301',
                        'runMode' : 'MANUAL'
                    }
                else :
                    reply = {
                        'what' : 'SET_TASKMODE',
                        'code' : '3',
                        'errNo' : '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_TASKMODE':            # 6.1.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'GET_TASKMODE',
                        'code' : '0',
                        'taskID' : '301',
                        'runMode' : 'MANUAL'
                    }
                else :
                    reply = {
                        'what': 'GET_TASKMODE',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_SYSTASK':             # 6.1.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'GET_SYSTASK',
                        'code' : '0',
                        'first' : '1',
                        'number' : '2',
                        'task' : [
                            {
                                'taskID' : '301',
                                'runMode' : 'MANUAL'
                            },
                            {
                                'taskID': '302',
                                'runMode': 'MANUAL'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'GET_TASKMODE',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_TASKHISTORY':            # 6.1.4
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'GET_TASKHISTORY',
                        'code' : '0',
                        'days' : '7',
                        'day' : [
                            {
                               'number' : '2',
                                'record' : [
                                    {
                                        'recvTome': '2024-9-10 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-10 17:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '2',
                                'record': [
                                    {
                                        'recvTome': '2024-9-11 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-11 17:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '2',
                                'record': [
                                    {
                                        'recvTome': '2024-9-12 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-12 17:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '2',
                                'record': [
                                    {
                                        'recvTome': '2024-9-13 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-13 17:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '2',
                                'record': [
                                    {
                                        'recvTome': '2024-9-14 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-14 17:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '4',
                                'record': [
                                    {
                                        'recvTome': '2024-9-15 8:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-15 11:00:00',
                                        'runMode': 'STOP'
                                    },
                                    {
                                        'recvTome': '2024-9-15 14:00:00',
                                        'runMode': 'MANUAL'
                                    },
                                    {
                                        'recvTome': '2024-9-15 16:00:00',
                                        'runMode': 'STOP'
                                    }
                                ]
                            },
                            {
                                'number': '0',
                                'record': [
                                ]
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'GET_TASKHISTORY',
                        'code' : '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'SET_EQUIP':                   # 6.2.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'SET_EQUIP',
                        'code' : '0',
                        'number' : '2',
                        'equip' : [
                            {
                                'equipID': '30311',
                                'status': 'TURN-On'
                            },
                            {
                                'equipID': '30312',
                                'status': 'TURN-Off'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what' : 'SET_EQUIP',
                        'code' : '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_EQUIP':                  # 6.2.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'GET_EQUIP',
                        'code' : '0',
                        'first' : '1',
                        'number' : '2',
                        'equip' : [
                            {
                                'equipID': '30311',
                                'status': 'TURN-On'
                            },
                            {
                                'equipID': '30312',
                                'status': 'TURN-Off'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_EQUIPHISTORY':            # 6.2.3
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'GET_EQUIPHISTORY',
                        'code' : '0',
                        'days' : '7',
                        'day' : [
                            {
                                'number': '5',
                                'time' : [
                                    {
                                        'datetime': '2024-9-10 8:00:00',
                                        'paramNum' : '2',
                                        'param' : [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    },{
                                        'datetime': '2024-9-10 8:30:00',
                                        'paramNum' : '2',
                                        'param' : [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-11 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-11 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-12 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-12 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-13 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-13 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-14 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-14 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-15 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-15 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-16 8:00:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.0'
                                            },
                                            {
                                                'paramID': '2.0'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:10:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.1'
                                            },
                                            {
                                                'paramID': '2.1'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:20:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.3'
                                            },
                                            {
                                                'paramID': '2.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.5'
                                            },
                                            {
                                                'paramID': '2.5'
                                            }
                                        ]
                                    }, {
                                        'datetime': '2024-9-16 8:30:00',
                                        'paramNum': '2',
                                        'param': [
                                            {
                                                'paramID': '1.7'
                                            },
                                            {
                                                'paramID': '7.5'
                                            }
                                        ]
                                    }
                                ],
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'SET_NODEACTIVE':              # 6.3.1
                if data['systemID'] == '101':
                    reply = {
                        'what': 'SET_NODEACTIVE',
                        'code': '0',
                        'number' : '3',
                        'node' : [
                            {
                                'nodeID' : '1',
                                'status' : 'ENABLE'
                            },
                            {
                                'nodeID': '2',
                                'status': 'ENABLE'
                            },
                            {
                                'nodeID': '3',
                                'status': 'DISABLE'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'SET_NODEWAKEUP':              # 6.3.2
                if data['systemID'] == '101':
                    reply = {
                        'what': 'SET_NODEWAKEUP',
                        'code': '0',
                        'number' : '2',
                        'node' : [
                            {
                                'nodeID': '1',
                                'status': 'WAKEUP'
                            },
                            {
                                'nodeID': '2',
                                'status': 'SLEEP'
                            },
                       ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_NODESTATUS':              # 6.3.3
                if data['systemID'] == '101':
                    reply = {
                        'what': 'GET_NODESTATUS',
                        'code': '0',
                        'first' : '1',
                        'number' : '2',
                        'node' : [
                            {
                                'nodeID' : '1',
                                'status': 'ENABLE',
                                'powerVoltage': '3.289',
                                'loadCurrent': '1.298',
                                'rssi': '-90',
                                'snr': '2.3'
                            },
                            {
                                'nodeID': '2',
                                'status': 'ENABLE',
                                'powerVoltage': '4.089',
                                'loadCurrent': '2.298',
                                'rssi': '-80',
                                'snr': '7.3'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_NODEHISTORY':             # 6.3.4
                if data['systemID'] == '101':
                    reply = {
                        'what': 'GET_NODEHISTORY',
                        'code': '0',
                        'days' : '7',
                        'day' : [
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-10 8:00:00',
                                        'nodeNum': '2',
                                        'node' : [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-11 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-12 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-12 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-13 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-13 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-14 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-14 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-15 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-15 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                            {
                                'number': '5',
                                'time': [
                                    {
                                        'datetime': '2024-9-16 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:10:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:20:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:30:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-16 8:40:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                                'powerVoltage': '3.289',
                                                'loadCurrent': '1.298',
                                                'rssi': '-90',
                                                'snr': '2.3'
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                                'powerVoltage': '4.089',
                                                'loadCurrent': '2.298',
                                                'rssi': '-80',
                                                'snr': '7.3'
                                            }
                                        ]
                                    },
                                ],
                            },
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'GET_NODESTATUSHISTORY':       # 6.3.5
                if data['systemID'] == '101' :
                    reply = {
                        'what': 'GET_NODESTATUSHISTORY',
                        'code': '0',
                        'days' : '7',
                        'day' : [
                            {
                                'number': '4',
                                'time': [
                                    {
                                        'datetime': '2024-9-10 8:00:00',
                                        'nodeNum': '2',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                            },
                                            {
                                                'nodeID': '2',
                                                'status': 'ENABLE',
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:20:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '2',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-10 8:30:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '3',
                                'time': [
                                    {
                                        'datetime': '2024-9-11 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:20:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '2',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    },
                                    {
                                        'datetime': '2024-9-11 8:30:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'ENABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '1',
                                'time': [
                                    {
                                        'datetime': '2024-9-12 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '1',
                                'time': [
                                    {
                                        'datetime': '2024-9-13 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '1',
                                'time': [
                                    {
                                        'datetime': '2024-9-14 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '1',
                                'time': [
                                    {
                                        'datetime': '2024-9-15 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                            {
                                'number': '1',
                                'time': [
                                    {
                                        'datetime': '2024-9-1 8:10:00',
                                        'nodeNum': '1',
                                        'node': [
                                            {
                                                'nodeID': '1',
                                                'status': 'DISABLE',
                                            }
                                        ]
                                    }
                                ],
                            },
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'RPT_WHETHER':                 # 7.1.1
                dt = datetime.now()
                temp, humi = get_whether()
                reply = {
                    'what': 'RPT_WHETHER',
                    'code': 'PUBLISH',
                    'publish_time' : str(dt),
                    'temperature' : temp,
                    'humidity' : humi
                }
            elif data['todo'] == 'RPT_GENERAL':                 # 7.1.2
                reply = {
                    'what': 'RPT_GENERAL',
                    'code': 'PUBLISH',
                    'publish_time' : str(datetime.now()),
                    'energy_all' : '2167',
                    'water_all' : '8922',
                    'online_all' : '80',
                    'running_all' : '50',
                    'task_all' : '28',
                    'ex_task_all' : '20'
                }
            elif data['todo'] == 'RPT_TASKALL':                 # 7.2.1
                reply = {
                    'what': 'RPT_TASKALL',
                    'code': 'PUBLISH',
                    'publish_time' : str(datetime.now()),
                    'number' : '3',
                    'task' : [
                        {
                            'taskID' : '101',
                            'status' : 'MANUAL',
                            'startTime' : '2024-9-10 8:00:00',
                            'finishTime' : '2024-9-10 17:10:00',
                        },
                        {
                            'taskID': '102',
                            'status': 'STOP',
                            'startTime': '2024-9-10 8:00:00',
                            'finishTime': '2024-9-10 17:10:00',
                        },
                        {
                            'taskID': '103',
                            'status': 'AUTO',
                            'startTime': '2024-9-10 8:00:00',
                            'finishTime': '2024-9-10 17:10:00',
                        },
                    ]
                }
            elif data['todo'] == 'RPT_AREAENV':             # 7.2.2
                reply = {
                    'what': 'RPT_AREAENV',
                    'code': 'PUBLISH',
                    'publish_time' : str(datetime.now()),
                    'number' : '3',
                    'area' : [
                        {
                            'areaID' : '1001',
                            'temperature4' : '20.3',
                            'humidity4' : '80.9',
                            'brightness4' : '500',
                            'turbidity4' : '10'
                        },
                        {
                            'areaID': '1002',
                            'temperature4': '20.3',
                            'humidity4': '80.9',
                            'brightness4': '500',
                            'turbidity4': '10'
                        },
                        {
                            'areaID': '1003',
                            'temperature4': '20.3',
                            'humidity4': '80.9',
                            'brightness4': '500',
                            'turbidity4': '10'
                        },
                    ]
                }
            elif data['todo'] == 'RPT_EQUIPMENT':           # 7.2.3
                reply = {
                    'what': 'RPT_EQUIPMENT',
                    'code': 'PUBLISH',
                    'publish_time' : str(datetime.now()),
                    'devType' : '空调执行器',
                    'number' : '2',
                    'equip' : [
                        {
                            'equipID' : '101',
                            'status' : 'TURN-ON',
                            'areaID' : '1001'
                        },
                        {
                            'equipID': '102',
                            'status': 'TURN-OFF',
                            'areaID': '1002'
                        }
                    ]
                }
            elif data['todo'] == 'QRY_MEMBER':              # 8.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'QRY_MEMBER',
                        'code': '0',
                        'number' : '2',
                        'member' : [
                            {
                                'userID' : '10002'
                            },
                            {
                                'userID' : '1001'
                            }
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'SET_PERMIT':              # 8.2.1
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'SET_PERMIT',
                        'code': 'OK'
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_PERMITMEMBER':        # 8.2.2
                if data['systemID'] == '101':
                    reply = {
                        'what' : 'QRY_PERMITMEMBER',
                        'code': '0',
                        'number1' : '2',
                        'member' : [
                            {
                                'userID' : '10002',
                                'number2' : '2',
                                'area' : [
                                    {
                                        'areaID' : '1001',
                                        'number3' : '3',
                                        'equip' : [
                                            {
                                                'equipID' : '101',
                                                'permit' : 'R'
                                            },
                                            {
                                                'equipID' : '11002',
                                                'permit' : 'R'
                                            },
                                            {
                                                'equipID': '11012',
                                                'permit': 'N'
                                            }
                                        ]
                                    },
                                    {
                                        'areaID': '1002',
                                        'number3': '2',
                                        'equip': [
                                            {
                                                'equipID': '201',
                                                'permit': 'V'
                                            },
                                            {
                                                'equipID': '21002',
                                                'permit': 'N'
                                            }
                                        ]
                                    },
                                ]
                            },
                            {
                                'userID': '10001',
                                'number2': '2',
                                'area': [
                                    {
                                        'areaID': '1001',
                                        'number3': '3',
                                        'equip': [
                                            {
                                                'equipID': '101',
                                                'permit': 'R'
                                            },
                                            {
                                                'equipID': '11002',
                                                'permit': 'N'
                                            },
                                            {
                                                'equipID': '11012',
                                                'permit': 'N'
                                            }
                                        ]
                                    },
                                    {
                                        'areaID': '1002',
                                        'number3': '2',
                                        'equip': [
                                            {
                                                'equipID': '201',
                                                'permit': 'V'
                                            },
                                            {
                                                'equipID': '21002',
                                                'permit': 'R'
                                            }
                                        ]
                                    },
                                ]
                            },
                        ]
                    }
                else :
                    reply = {
                        'what': 'SET_EQUIP',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }
            elif data['todo'] == 'QRY_PERMITAREA':      # 8.2.3
                if data['systemID'] == '101':
                    reply = {
                        'what': 'QRY_PERMITAREA',
                        'code': '0',
                        'number1' : '2',
                        'area' : [
                            {
                                'areaID' : '1001',
                                'number2' : '2',
                                'equip' : [
                                    {
                                        'equipID' : '101',
                                        'number3' : '2',
                                        'member' : [
                                            {
                                                'userID' : '1002',
                                                'permit' : 'R'
                                            },
                                            {
                                                'userID' : '11012',

                                            }
                                        ]
                                    },
                                    {
                                        'equipID': '102',
                                        'number3': '2',
                                        'member': [
                                            {
                                                'userID': '1002',
                                                'permit': 'R'
                                            },
                                            {
                                                'userID': '11012',

                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                'areaID': '1001',
                                'equip': [
                                    {
                                        'equipID': '101',
                                        'number3': '2',
                                        'member': [
                                            {
                                                'userID': '1002',
                                                'permit': 'R'
                                            }
                                        ]
                                    },
                                ]
                            },
                        ]
                    }
                else :
                    reply = {
                        'what': 'QRY_PERMITAREA',
                        'code': '3',
                        'errNo': '999',
                        'errMsg': '错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述，错误代码描述'
                    }

            if len(reply) > 0:
                logging.info('Reply: ' + str(reply) + '\n')

            # send_data = 'Hello %s' % recv_data
            send_data = json.dumps(reply)
            await accept.send(send_data)

        except json.JSONDecodeError:
            # 如果数据不是有效的 JSON，处理错误
            data = json.loads(recv_data)
            reply = {
                'what': str(data['todo']),
                'code': '1',
                'errNo': 'unknown requirement'
            }
            await accept.send(json.dumps(reply))
        except KeyError:
            # 如果数据中没有 'todo' 键，处理错误
            data = json.loads(recv_data)
            reply = {
                'what': str(data['todo']),
                'code': '1',
                'errNo': 'unknown requirement'
            }
            await accept.send(json.dumps(reply))
        except Exception as e:
            await accept.send(json.dumps(e))

async def start():
    print('Server started ...')

    # web_socket_server = websockets.serve(websocket, "0.0.0.0", 9902)
    #
    # asyncio.get_event_loop().run_until_complete(web_socket_server)
    # asyncio.get_event_loop().run_forever()

    async with websockets.serve(websocket, '0.0.0.0', 9902):
        await asyncio.Future()

# if __name__ == '__main__':
#     asyncio.run(start())
