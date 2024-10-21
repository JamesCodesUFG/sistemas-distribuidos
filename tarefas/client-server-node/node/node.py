import os

import socket
from socket import socket as Socket

from math import ceil

from utils.system import *
from utils.protocol import *

class Node(System):
    __socket: Socket = None
    __broadcast: Socket = None

    def __init__(self):
        super().__init__()

        self.daemon = True

        self.__create_socket()

        sys.set_int_max_str_digits(10000)

    def exit(self):
        pass

    def run(self):
        while True:
            request = Request.decode(self.server_socket.recv(BUFFER_SIZE))

            self._logger.log(request.to_string())

            match request.method:
                case RequestMethod.GET:
                    self.__get(request)
                case RequestMethod.POST:
                    self.__post(request)
                case RequestMethod.DELETE:
                    self.__delete(request)

    def __get(self, request: Request):
        data = self.__read(request.path)

        self.server_socket.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
            if inner % 500 == 0 or inner == ceil(len(data) / BUFFER_SIZE) - 1:
                self._logger.log(f'Enviado {inner} de {ceil(len(data) / BUFFER_SIZE)}.')

            self.server_socket.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        self._logger.log(f'Envio finalizado com sucesso...')

    def __post(self, request: Request):
        data = b''

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            if inner % 500 == 0:
                self._logger.log(f'Recebido {inner} de {ceil(request.lenght / BUFFER_SIZE)}.')

            data = data + self.server_socket.recv(BUFFER_SIZE)

        self._logger.log('Todos os dados foram recebidos...')

        self.__write(request.path, data)

        self._logger.log('Post finalizado com sucesso...')

    def __delete(self, request: Request):
        os.remove('./node/images' + request.path)

    def __create_socket(self) -> None:
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            new_socket.bind(('127.0.0.1', 0))

            new_socket.listen(4)

            self.__socket = new_socket

            self._logger.log(f'[SERVER] {new_socket.getsockname()}')
        except Exception as error:
            self._logger.error(f'[SERVER] {error}')

    def __create_broadcast(self):
        try:
            new_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            new_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            new_broadcast.bind(self.__socket.getpeername())

            new_broadcast.settimeout(0.5)

            self.__broadcast = new_broadcast

            self._logger.log(f'[BROADCAST] {new_broadcast.getsockname()}')
        except Exception as error:
            self._logger.error(f'[BROADCAST] {error}')

    def __find_server(self):
        while self.__ping_server(self.__socket.getsockname()) != 'PONG':
            self.__braodcast.sendto('PING'.encode(), ('<broadcast>', 8080))

            data, _ = new_broadcast.recvfrom(1024)

            return data.decode()
        else:
            _, address = self.__socket.accept()
            self.server_address = address

    def __ping_server(self, address: tuple) -> str:
        
    
    def __read(self, file_name: str) -> bytes:
        data: bytes = None

        self._logger.log(f"Lendo arquivo '{file_name}'")

        with open('./node/images' + file_name, 'rb') as file:
            data = file.read()

        self._logger.log("Leitura finalizada com sucesso...")

        return data

    def __write(self, file_name: str, data: bytes) -> None:
        self._logger.log(f"Escrevendo arquivo '{file_name}'")

        with open('./node/images' + file_name, 'wb') as file:
            file.write(data)

        self._logger.log("Escrita finalizada com sucesso...")
    
SystemManager(Node())