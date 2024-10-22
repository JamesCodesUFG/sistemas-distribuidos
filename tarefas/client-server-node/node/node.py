import os
from math import ceil

import socket
from socket import socket as Socket

from threading import Thread

from utils.system import *
from utils.protocol import *
from utils.file_manager import *

class Node(System):
    __file: FileManager = FileManager()

    __socket: Socket = None
    __broadcast: Socket = None

    def __init__(self):
        super().__init__()

        self.daemon = True

        self.__create_socket()
        self.__create_broadcast()

        self.__ping_server()

    def exit(self):
        pass

    def run(self):
        while True:
            client, address = self.__socket.accept()

            if self.__server_address == address:
                thread = Thread(target=self.__handle_request, args=(client, ), daemon=True)

                thread.start()
            else:
                self._logger.warning(f'Cliente desconhecido: {address}')

    def __handle_request(self, client: Socket):
        request = Request.decode(self.__socket.recv(BUFFER_SIZE))

        self._logger.log(f'[REQUEST] {client.getpeername()}, {request}')

        try:
            match request.method:
                case RequestMethod.GET:
                    self.__get(client, request)
                case RequestMethod.POST:
                    self.__post(client, request)
                case RequestMethod.DELETE:
                    self.__delete(client, request)
                case _:
                    self._logger.error(f'Caso não mapeado: {request.method}')
        except Exception as error:
            self._logger.error(error)

    def __get(self, client: Socket, request: Request):
        data = self.__file.read(request.path)

        client.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
            client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        client.close()

        self._logger.log('[SUCESSO] Arquivo guardado...')

    def __post(self, client: Socket, request: Request):
        data = b''

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            data = data + self.__socket.recv(BUFFER_SIZE)

        self.__file.write(request.path, data)

        client.close()

        self._logger.log('[SUCESSO] Arquivo enviado...')

    def __delete(self, client: Socket, request: Request):
        self.__file.delete(request.path)

        client.send(Response(ResponseCode.OK))

        client.close()

        self._logger.log('[SUCESSO] Arquivo deletado...')

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

    def __ping_server(self):
        for inner in range(0, 3):
            self._logger.log(f'[PING] Tentativa {inner + 1} de 3.')

            self.__broadcast.sendto('PING'.encode(), ('<broadcast>', 8080))

            data, address = self.__broadcast.recvfrom(1024)

            if data.decode() == 'PONG':
                self.__server_address = address
                return
            else:
                self._logger.warning(f'[PING] Remetente desconhecido...')

        self._logger.error(f'[PING] Servido não encontrado...')
        raise Exception('Servido não encontrado...')
    
SystemManager(Node())