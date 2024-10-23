import os
from math import ceil

import socket
from socket import socket as Socket

from threading import Thread

from utils.system import *
from utils.protocol import *
from utils.file_manager import *

class Node(System):
    __file: FileManager = FileManager(r'C:\Users\tiago\Documents\Workflows\ufg\sistemas-distribuidos\tarefas\client-server-node\node\images')

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

            if self.__server_address[0] == address[0]:
                thread = Thread(target=self.__handle_request, args=(client, ), daemon=True)

                thread.start()
            else:
                self._logger.warning(f'[DESCONHECIDO] {address}')

    def __handle_request(self, client: Socket):
        request = Request.decode(client.recv(BUFFER_SIZE))

        self._logger.log(f'[REQUEST] {client.getsockname()}, {request}')

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
            client.send(Response(ResponseCode.ERROR).encode())

            self._logger.error(f'[ERROR] {error}')
        else:
            client.send(Response(ResponseCode.SUCCESS).encode())

            self._logger.log('[SUCCESS] Requisição concluida...')
        finally:
            client.close()

    def __get(self, client: Socket, request: Request):
        data = self.__file.read(request.path)

        client.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
            client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    def __post(self, client: Socket, request: Request):
        data = b''

        response = client.send(Response(ResponseCode.READY).encode())

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            if inner%10 == 0:
                self._logger.log(f'[POST] {inner + 1} de {ceil(request.lenght / BUFFER_SIZE)}')

            data = data + client.recv(BUFFER_SIZE)

        self.__file.write(request.path, data)

    def __delete(self, client: Socket, request: Request):
        try:
            self.__file.delete(request.path)

            client.send(Response(ResponseCode.OK).encode())
        except Exception as error:
            raise Exception('[DELETE]', error)

    def __create_socket(self) -> None:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        new_socket.bind(('127.0.0.1', 0))

        new_socket.listen(4)

        self.__socket = new_socket

        self._logger.log(f'[SERVER] {new_socket.getsockname()}')

    def __create_broadcast(self):
        new_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        new_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        new_broadcast.bind(self.__socket.getsockname())

        new_broadcast.settimeout(0.1)

        self.__broadcast = new_broadcast

        self._logger.log(f'[BROADCAST] {new_broadcast.getsockname()}')

    def __ping_server(self):
        for inner in range(0, 3):
            try:
                self._logger.log(f'[PING] Tentativa {inner + 1} de 3.')

                self.__broadcast.sendto('PING'.encode(), ('<broadcast>', 8080))

                data, address = self.__broadcast.recvfrom(1024)

                if data.decode() == 'PONG':
                    self.__server_address = address
                    self._logger.log(f'[PING] Servidor encontrado: {address}')
                    return
                else:
                    self._logger.warning(f'[PING] Remetente desconhecido...')
            except:
                pass

        raise Exception('[PING] Servidor não encontrado...')
    
SystemManager(Node())