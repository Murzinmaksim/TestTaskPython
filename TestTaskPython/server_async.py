import asyncio
import random
import time
import logging

clients = {}  # Словарь для хранения подключенных клиентов
clients_count = 1
response_count = 0  # Счетчик ответов сервера
request_time = None  # Задаем переменной значение по умолчанию

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(message)s', encoding='utf-8')

async def handle_client(reader, writer):
    global response_count, clients_count, request_time  # Объявляем переменные как глобальные
    address = writer.get_extra_info('peername')  # Получаем информацию об адресе клиента
    print(f"Принято соединение от {address}")

    clients[clients_count] = writer  # Добавляем клиента в словарь
    clients_count += 1

    try:
        while True:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S:{:03.0f}'.format(time.time()%1000), time.localtime())
            # С вероятностью 10% игнорируем запрос
            if random.random() < 0.1:
                str = "(проигнорировано)"
                print("Сервер проигнорировал запрос")
                logging.info(f"{current_time}; {str}; {str}")
                continue  # Продолжаем ожидать следующего сообщения от клиента

            data = await reader.readline()  # Читаем строку данных от клиента
            message = data.decode('ascii').strip()
            request_time = current_time
            print(f"{current_time} - {message}")

            # Генерируем случайный интервал от 100 до 1000 мс
            response_delay = random.uniform(0.1, 1)
            await asyncio.sleep(response_delay)

            # Формируем ответное сообщение с уникальным номером ответа
            for key, value in clients.items():
                if value == writer:
                    response_message = f"PONG [{response_count}] ({key})"
            writer.write(response_message.encode('ascii'))
            await writer.drain()
            response_time = time.strftime('%Y-%m-%d %H:%M:%S.{:03.0f}'.format(time.time()%1000), time.localtime())
            print(f"{current_time} - {response_message.strip()}")

            logging.info(f"{request_time}; {message}; {response_time}; {response_message}")

            response_count += 1  # Увеличиваем счетчик ответов
    finally:
        for key, value in clients.items():
                if value == writer:
                    del clients[key]
        print(f"Соединение с {address} закрыто")

async def send_keepalive_to_clients():
    global response_count  # Объявляем переменную как глобальную
    while True:
        await asyncio.sleep(5)  # Ожидаем 5 секунд
        for key, writer in clients.items():
            keepalive_message = f"[{response_count}] keepalive\n"
            writer.write(keepalive_message.encode('ascii'))
            await writer.drain()  # Дожидаемся завершения записи в соединение
            print(f"Отправлено keepalive клиенту: {keepalive_message.strip()}")
        response_count += 1

async def start_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        print(f"Сервер запущен на {host}:{port}")
        asyncio.create_task(send_keepalive_to_clients())
        await server.serve_forever()

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    asyncio.get_event_loop().run_until_complete(start_server(HOST, PORT))