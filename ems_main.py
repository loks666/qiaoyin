#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#---------------------------
# import
import os
import threading
import json
import logging
import pymysql
from time import ctime, sleep
from anyio import value

from ems_base import (MyThread, network, ems_db, ems_ds, ems_buf, network, gen_token, gen_md5)

"""
db_conn = pymysql.connect(host = ems_ds['host'], port = ems_ds['port'], user = ems_ds['user'],
                         passwd = ems_ds['password'], db = ems_ds['database'], charset = ems_ds['charset'])
cursor = db_conn.cursor()

db_list = cursor.execute('show databases; ')
tab_list = cursor.execute('show tables; ')
"""

#---------------------------
# initiate network


def lora_sub (a, b):
    while True :
        # print('lora_sub')
        sleep(10)

def lora_pub (a, b):
    while True :
        # print('lora_pub')
        sleep(10)

def lora_mon (a, b):
    while True :
        # print('lora_mon')
        sleep(10)

def lora_proc (a, b):
    while True :
        # print('lora_mqtt')
        sleep(10)

def sche_exe (a, b):
    while True :
        # print('sche_exec')
        sleep(10)

def sche_mon (a, b):
    while True :
        # print('sche_mon')
        sleep(10)

from web_recv import web_recv
from web_tran import web_tran
"""
def web_recv (a, b):
    while True :
        # print('web_recv')
        sleep(10)

def web_tran (a, b):
    while True :
        # print('web_tran')
        sleep(10)
"""

def web_proc (a, b):
    while True :
        # print('web_proc')
        sleep(10)

def host_recv (a, b):
    while True :
        # print('host_recv')
        sleep(10)

def host_tran (a, b):
    while True :
        # print('host_tran')
        sleep(10)

def host_proc (a, b):
    while True :
        # print('host_proc')
        sleep(10)

def conn_mgmt (a, b):
    while True :
        # print('conn_mgmt')
        sleep(10)

from db_query import db_query
"""
def db_query (a, b):
    while True :
        print('db_query')
        sleep(10)
"""

def db_sync (a, b):
    while True :
        # print('db_sync')
        sleep(10)

thread_list = [lora_sub, lora_pub, lora_mon, lora_proc, sche_exe, sche_mon, web_recv, web_tran, web_proc,
               host_recv, host_tran, host_proc, conn_mgmt, db_query, db_sync]
nthread_list = range(len(thread_list))
thread = []

def generate_thread() :
    for i in nthread_list:
        t = MyThread(thread_list[i], (1, 0), thread_list[i].__name__, True)
        thread.append(t)

    for i in nthread_list:
            thread[i].start()

def stop_all_threads() :
    for i in nthread_list:
        thread[i].join()


if __name__ == '__main__' :
    # initiate logfile
    logging.critical('\n\n\tsystem is now booting ......\n')

    from db_query import db_query, init_buffer_cache, init_buffer_sche
    init_buffer_cache()
    init_buffer_sche()
    # get_network()



    from web_tran import web_tran
    from web_recv import web_recv

    # initiate threads
    generate_thread()
    stop_all_threads()