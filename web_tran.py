import asyncio
from datetime import datetime, timedelta
import ems_verify_sms
import json
from time import sleep
from ems_base import ems_db_conn, ems_recv
import logging
import web_recv

async def recycle():
    clients = web_recv.clients

    while (True):
        if (len(clients) <= 0):
            await asyncio.sleep(1)
            continue

        with ems_db_conn._ems_db__pool.connection() as con:
            with con.cursor() as cursor:

                # 获取回传数据
                cursor.execute("select * from mem_web_socket_transit limit 100")
                rows = cursor.fetchall()

                for row in rows:
                    # 回传数据结构
                    action = json.loads(row['send_data'])
                    if ('todo' in action):
                        for client in clients:
                            content = ''
                            if (action['todo'] == 'SET_SUPERLOGIN'):
                                sql = ("select * from verify_code "
                                       "where user_name='%s' and user_passwd='%s' and verify_code='%s'")
                                content = {'what': 'SET_SUPERLOGIN', 'code': 'OK', 'MEMO': 'from server'}

                            if (action['todo'] == 'QRY_SUPERSYSTEM'):
                                content = {'what': 'QRY_SUPERSYSTEM', 'code': 'OK', 'systemID': '1',
                                           'MEMO': 'from server'}

                            if (action['todo'] == 'SET_SUPERPNGFILE'):
                                content = {'what': 'SET_SUPERPNGFILE', 'code': 'OK', 'systemID': '1',
                                           'MEMO': 'from server'}

                            if (action['todo'] == 'GET_SUPERVERIFY'):
                                minutes_to_add = 5
                                current_time = datetime.now()
                                time_delta = timedelta(minutes=minutes_to_add)
                                extended_time = current_time + time_delta

                                code = ems_verify_sms.gen_verify_code()     # generate a verify code
                                sql = "insert into verify_code values(%s,%s,%s,%s,%s)"  # keep into table
                                cursor.execute(sql, (extended_time,action['superName'],action['superPasswd'],
                                                     action['phone_no'],code))
                                ems_verify_sms.send_verify_code(str(action['phone_no']),str(code))  # send out

                                content = {'what': 'GET_SUPERVERIFY', 'code': 'OK'}

                            con.commit()
                            if (len(content) > 0):
                                send_data = json.dumps(content)
                                logging.info(' send to websocket: ' + str(send_data))
                                await client.send(send_data)
            con.close()
        await asyncio.sleep(1)


def transit():
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(recycle())
    asyncio.get_event_loop().run_forever()


#threading.Thread(target=transit).start()

def web_tran (a, b):
    # sleep(5)
    transit()
    """
    while True :
        print('web_tran')
        sleep(0.001)
    """
