import asyncio
import os
import signal

import websockets
import json
from datetime import datetime
import pytz

async def echo(websocket, path): # обработка входящего сообщения
    data_set = {}
    async for message in websocket:
        print("Inbound message:\t", message)
        converted = pytz.timezone('Europe/Moscow')
        data_set["time"] = datetime.now(converted).strftime("%H:%M")
        if (message=="Текст"):
            data_set["content"] = "Пример текстового сообщения"
            json_data = json.dumps(data_set)
            await websocket.send(json_data)
        elif (message=="Бот"):
          data_set["content"] = "Бот поддерживает команды \"Текст\", \"Привет\" и \"Погода\""
          json_data = json.dumps(data_set)
          await websocket.send(json_data)
        elif (message=="Привет"):
          data_set["content"] = "Как дела?"
          json_data = json.dumps(data_set)
          await websocket.send(json_data)
        elif (message=="Погода"):
          data_set["content"] = "Мороз и солнце, день чудесный!"
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
