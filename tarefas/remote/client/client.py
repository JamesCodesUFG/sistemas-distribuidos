import sys
import os

import rpyc

from utils.file_manager import FileManager

class Client:
    __file_manager: FileManager = FileManager('images')

    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.__host = host
        self.__port = port

        self.loop()

    def loop(self) -> None:
        while True:
            _input = self.input()

            match (_input[0]):
                case 'get':
                    self.get(_input[1])
                case 'post':
                    self.post(_input[1])
                case 'list':
                    self.list()
                case 'delete':
                    self.delete(_input[1])

    def get(self, name: str) -> None:
        file = self.__connect().get(name)

        self.__file_manager.write(name, file)

    def post(self, name: str) -> None:
        file = self.__file_manager.read(name)

        self.__connect().post(name, file)

    def list(self) -> None:
        names = self.__connect().list()

        print(f'{names}\n')

    def delete(self, name: str) -> None:
        self.__connect().delete(name)

    def input(self) -> tuple:
        input_data = input('> ')

        input_list = input_data.split(' ')

        return (input_list[0], input_list[1] if input_list[0] != 'list' else '')
    
    def __connect(self):
        try:
            self.__geoeye.ping()
        except:
            print(f'\n[WARNING] Restabelecendo conexão com servidor...')

            self.__geoeye = rpyc.connect(self.__host, self.__port)
        finally:
            return self.__geoeye.root
    
Client()