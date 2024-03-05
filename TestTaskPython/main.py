import concurrent.futures
import subprocess
import os
import time

scripts_to_run = [
    "server_async.py",
    "client_async.py",
    "client_async.py"
]

# Функция для запуска скрипта с таймером
def run_script_with_timeout(script):
    start_time = time.time()
    process = subprocess.Popen(["python", script])
    try:
        # Ожидание завершения процесса или прерывание по истечении времени
        process.wait(timeout=300) 
    except subprocess.TimeoutExpired:
        print(f"Скрипт {script} прерван из-за превышения времени выполнения.")
        os.kill(process.pid, 9)  # Прерываем выполнение процесса, если превышен таймаут
    end_time = time.time()
    print(f"Время выполнения скрипта {script}: {end_time - start_time} секунд.")

# Создание пула потоков для выполнения скриптов параллельно
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(run_script_with_timeout, scripts_to_run)