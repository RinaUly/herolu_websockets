import asyncio
import os
import signal

import websockets
import json
from datetime import datetime

async def echo(websocket, path): # обработка входящего сообщения
    data_set = {}
    async for message in websocket:
        print("Inbound message:\t", message)
        data_set["time"] = datetime.now().strftime("%H:%M")
        if (message=="Текст"):
            data_set["content"] = "Пример текстового сообщения"
            json_data = json.dumps(data_set)
            await websocket.send(json_data)
        elif (message=="Бот"):
          data_set["content"] = "Бот поддерживает команды \"Текст\" и еще некоторые другие, с которыми я баловалась"
          json_data = json.dumps(data_set)
          await websocket.send(json_data)
        elif (message == "e"):
            data_set["content"] = "Shrek is love, shrek is life"
            json_data = json.dumps(data_set)
            await websocket.send(json_data)
        elif (message == "f"):
            data_set["content"] = "pay respect"
            json_data = json.dumps(data_set)
            await websocket.send(json_data)
        else:
            data_set["content"] = "Сообщение не распознано."
            json_data = json.dumps(data_set)
            await websocket.send(json_data)
async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    async with websockets.serve(
        echo,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
# start_server = websockets.serve(echo, "0.0.0.0", 80)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
