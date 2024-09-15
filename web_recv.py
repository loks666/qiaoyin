import asyncio
import json
import websockets
import pymysql.cursors
import logging
from datetime import datetime, timedelta
from ems_base import ems_db, ems_recv, ems_db_conn, LOG_FORMAT, network, web_conn
from time import ctime, sleep
clients = []

class WebServer:

    def __init__(self, host, port):
        global clients
        self.host = host
        self.port = port
        self.clients = clients

    def _save_mem_web_socket_receipt(self, data):
        try:
            # em = ems_db()
            recv_text = data
            data = json.loads(recv_text)
            logging.info(' receive from websocket: ' + str(data))
            user_id = data.get('user_id', 0)
            system_id = data.get('system_id', 0)
            need_answer = data.get('needAnswer')
            if (need_answer.upper() == 'NO'):
                need_answer = 'N'
            else:
                need_answer = 'Y'

            now = datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = ('insert into mem_web_socket_receipt (user_id, system_id, recv_time, recv_data,need_answer) '
                   'value(%s,%s,%s,%s,%s)')
            # em.execute(sql, (user_id, system_id, formatted_time, recv_text, need_answer))
            ems_db_conn.execute(sql, (user_id, system_id, formatted_time, recv_text, need_answer))
            # em._conn.commit()
            ems_db_conn._conn.commit()
        except Exception as e:
            logging.error('save mem_web_socket_receipt: ' + str(e))
            # print(e)

    async def recv(self, websocket, path):
        self.clients.append(websocket)
        client_ip, client_port = websocket.remote_address
        logging.info(f"connect to:{client_ip}:{client_port}")
        # print(f"连接到:{client_ip}:{client_port}")

        while True:
            try:
                recv_text = await websocket.recv()
                self._save_mem_web_socket_receipt(recv_text)

            except websockets.ConnectionClosed:
                logging.warning("Websocket was ConnectionClosed ...")
                # print("ConnectionClosed...")  # 链接断开
                if (websocket in self.clients):
                    self.clients.remove(websocket)
                break
            except websockets.InvalidState:
                logging.warning("Websocket is with InvalidState ...")
                # print("InvalidState...")  # 无效状态
                if (websocket in self.clients):
                    self.clients.remove(websocket)
                break
            except Exception as e:
                logging.error('Websocket connection error: ' + str(e))
                # print(e)

    def connect(self):
        logging.info(f"connect success！host={self.host}  port={self.port}")
        # print(f"连接成功！host={self.host}  port={self.port}")
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(self.recv, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    # def run(self):
    #    threading.Thread(target=self.connect).start()

def web_recv (a, b):
    web_socket = WebServer(web_conn['web_ip'], web_conn['web_port'])
    web_socket.connect()
    while True :
        sleep(0.001)