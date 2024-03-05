import asyncio
import random
import datetime
import logging
import os
import time

async def send_message(host, port):
    pid = os.getpid()  # Получаем идентификатор процесса (PID) текущего клиента
    log_filename = f'client_{pid}.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s; %(message)s', encoding='utf-8')
    
    reader, writer = await asyncio.open_connection(host, port)
    print(f"Connected to server at {host}:{port}")

    message_count = 0
    while True:
        message = f"[{message_count}] PING\n"
        timestamp_sent = time.strftime('%Y-%m-%d %H:%M:%S:{:03.0f}'.format(time.time()%1000), time.localtime())
        writer.write(message.encode('ascii'))
        await writer.drain()
        print(f"Sent message: {message.strip()}")
        message_count += 1

        # Принимаем сообщение от сервера
        response = await reader.readline()
        if response:
            str = response.decode('ascii').strip()
            timestamp_received = time.strftime('%Y-%m-%d %H:%M:%S:{:03.0f}'.format(time.time()%1000), time.localtime())
            print(f"Received response from server: {str}")
            logging.info(f"{timestamp_sent}; {message.strip()}; {timestamp_received}; {response.decode().strip()}")
            if str.endswith("keepalive"):
                 logging.info(f"(); (); {timestamp_received}; {response.decode().strip()}")

        # Генерация случайного интервала для отправки сообщения
        await asyncio.sleep(random.uniform(0.3, 3))

    writer.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    asyncio.get_event_loop().run_until_complete(send_message(HOST, PORT))