import sys

from threading import Thread

from abc import ABC, abstractmethod

from .logger import Logger

class System(Thread, ABC):
    _logger: Logger = Logger()

    @abstractmethod
    def exit():
        pass

    @abstractmethod
    def run(self):
        pass

    def kill(self):
        self.exit()
        sys.exit(1)

    def log(self):
        self._logger.print()

class SystemManager:
    __system: 'System' = None

    def __init__(self, system: 'System'):
        self.__system = system

        self.__system.start()

        self.__main_loop()

    def __main_loop(self):
        while True:
            _input = input('> ')

            if _input == 'exit' or _input == 'EXIT':
                self.__system.kill()
            elif _input == 'log' or _input == 'LOG':
                self.__system.log()