import os
import time
import psutil
import threading

from utils.rabbit import rabbit_single_send

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
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'CPU', 'status': 'HEAT' })
            elif self.__state and cpu_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'CPU', 'status': 'COLD' })
        
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
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'RAM', 'status': 'HEAT' })
            elif self.__state and ram_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'RAM', 'status': 'COLD' })
        
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

            if self.__state and disk_usage_percent >= self.__limit:
                self.__state = True
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'HDD', 'status': 'HEAT' })
            elif not self.__state and disk_usage_percent < self.__limit - OFF_SET:
                self.__state = False
                rabbit_single_send('monitor', { 'node': self.__name, 'comp': 'HDD', 'status': 'COLD' })

            time.sleep(2)

    def stop(self):
        self.__flag = False


