import asyncio
import datetime
import random
from time import sleep

from websockets.asyncio.server import broadcast, serve

# CONNECTIONS = set()
CONNECTIONS = []
n = 0

async def register(websocket):
    # CONNECTIONS.add(websocket)
    CONNECTIONS.append(websocket)
    l = len(CONNECTIONS)
    print('register ' + str(CONNECTIONS) + str(len(CONNECTIONS)))
    await websocket.send(str(CONNECTIONS[l - 1]))
    try:
        await websocket.wait_closed()
        print('try ' + str(CONNECTIONS))
    finally:
        CONNECTIONS.remove(websocket)
        print('remove ' + str(CONNECTIONS))

async def show_time():
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)

async def main():
    async with serve(register, "localhost", 5678):
        await show_time()

if __name__ == "__main__":
    asyncio.run(main())