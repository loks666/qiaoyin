#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
线程名称
UI接口
    web_recv    # websocket 接收线程
    web_tran    # websocket 发送线程
    web_proc    # websocket 接收缓存区处理线程
LoRa MQTT接口
    lora_sub    # lora MQTT 订阅线程
    lora_pub    # lora MQTT 发布现场
    lora_mon    # lora MQTT 发送线程回复监控线程
    lora_proc   # lora MQTT 接收缓存区处理线程
Cloud/host MQTT接口
    host_recv   # host MQTT 订阅线程
    host_tran   # host MQTT 发布线程
    host_proc   # host MQTT 接收缓存区处理线程
登录连接管理
    conn_mgmt   # web, lora, host 登录链接管理线程
定制计划
    sche_mon    # 计划执行监控线程
    sche_exe    # 计划执行线程
数据库
    db_query    # 数据查询线程
    db_sync     # 数据同步线程

ems_verify_sms.py
    gen_verify_code()   # 生产6位非0首的检验码
    send_verify_code(phone_num, verify_code)    # 发送校验码

ems_base.py
    LOG_FORMAT  # 日志输出格式
        写日志方法
            logging.debug('this is print_hi debug')
            logging.info('this is print_hi info')
            logging.warning('this is print_hi warning')
            logging.error('this is print_hi error')
            logging.critical('this is print_hi critical')
    gen_token(phone_num， user_name)     # 生成token
    gen_md5(file_name)      # 生产文件的MD5

    class ems_db()

mysql global variable
    db_conn
    db_cursor
    conn_db()
    close_db()
    db_exec()
    fetch_one()
    fetch_all()




"""
