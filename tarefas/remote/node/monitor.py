import os
import time
import psutil
import threading

from utils.rabbit import rabbit_send

OFF_SET = 0.3

class CPUMonitor(threading.Thread):
    def __init__(self, limit: float, name: str) -> None:
        super().__init__(daemon=True)

        self.__flag = True
        self.__state = False

        self.__process = psutil.Process(os.getpid())

        self.__limit = limit
        self.__name = name


    def run(self) -> None:
        while self.__flag:
            cpu_percent = self.__process.cpu_percent(interval=1)

            if not self.__state and cpu_percent >= self.__limit:
                self.__state = True
                rabbit_send('monitor', f'{self.__name} CPU HEAT')
            elif self.__state and cpu_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_send('monitor', f'{self.__name} CPU COLD')
        
            print(f"Uso da CPU pelo processo Python: {cpu_percent:.2f}%")

    def stop(self):
        self.__flag = False

class RAMMonitor(threading.Thread):
    def __init__(self, limit: float, name: str) -> None:
        super().__init__(daemon=True)

        self.__flag = True
        self.__state = False

        self.__limit = limit
        self.__name = name

    def run(self) -> None:
        while self.__flag:
            virtual_memory = psutil.virtual_memory()
        
            ram_percent = virtual_memory.percent

            if not self.__state and ram_percent >= self.__limit:
                self.__state = True
                rabbit_send('monitor', f'{self.__name} RAM HEAT')
            elif self.__state and ram_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_send('monitor', f'{self.__name} RAM COLD')
        
            print(f"Porcentagem de RAM usada: {ram_percent}%")

            time.sleep(2)

    def stop(self):
        self.__flag = False

class HDDMonitor(threading.Thread):
    def __init__(self, limit: float, name: str) -> None:
        super().__init__(daemon=True)

        self.__flag = True
        self.__state = False

        self.__limit = limit
        self.__name = name

    def run(self) -> None:
        while self.__flag:
            disk_usage = psutil.disk_usage('/')

            espaco_usado = disk_usage.used / (1024 ** 3)
            espaco_total = disk_usage.total / (1024 ** 3)

            disk_usage_percent = disk_usage.percent

            if not self.__state and disk_usage_percent >= self.__limit:
                self.__state = True
                rabbit_send('monitor', f'{self.__name} HDD HEAT')
            elif self.__state and disk_usage_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_send('monitor', f'{self.__name} HDD COLD')
        
            print(f"Espaço no HD: {espaco_usado:.2f} GB de {espaco_total:.2f} GB usados ({disk_usage_percent}% de uso)")

            time.sleep(2)

    def stop(self):
        self.__flag = False


