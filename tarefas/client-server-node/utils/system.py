from abc import ABC, abstractmethod

from threading import Thread

import sys

class Logger:
    def __init__(self):
        pass

class System(Thread, ABC):
    logger: 'Logger' = Logger()

    @abstractmethod
    def exit():
        pass

    #@abstractmethod
    #def log():
    #    pass

    @abstractmethod
    def run(self):
        pass

    def kill(self):
        self.exit()

        sys.exit()

class SystemManager:
    __system: 'System' = None

    def __init__(self, system: 'System'):
        self.__system = system

        self.__system.start()

        self.__main_loop()

    def __main_loop(self):
        while True:
            _input = input('> ')

            if _input == 'exit' or 'EXIT':
                self.__system.kill(1)
            elif _input == 'log' or 'LOG':
                print('Soon...')