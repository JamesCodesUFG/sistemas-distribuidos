import os
import socket

from math import ceil

from utils.system import *
from utils.protocol import *

class Node(System):
    server_socket: socket.socket = None

    def __init__(self):
        super().__init__()

        self.daemon = True

        self.__create_node_socket()

        sys.set_int_max_str_digits(10000)

    def exit(self):
        pass

    def run(self):
        while True:
            request = Request.decode(self.server_socket.recv(BUFFER_SIZE))

            self._logger.log(request.to_string())

            match request.method:
                case RequestMethod.GET:
                    self.__handle_get(request)
                case RequestMethod.POST:
                    self.__handle_post(request)
                case RequestMethod.DELETE:
                    self.__handle_delete(request)

    def __handle_get(self, request: Request):
        data = self.__read(request.path)

        self.server_socket.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
            if inner % 500 == 0 or inner == ceil(len(data) / BUFFER_SIZE) - 1:
                self._logger.log(f'Enviado {inner} de {ceil(len(data) / BUFFER_SIZE)}.')

            self.server_socket.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        self._logger.log(f'Envio finalizado com sucesso...')

    def __handle_post(self, request: Request):
        data = b''

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            if inner % 500 == 0:
                self._logger.log(f'Recebido {inner} de {ceil(request.lenght / BUFFER_SIZE)}.')

            data = data + self.server_socket.recv(BUFFER_SIZE)

        self._logger.log('Todos os dados foram recebidos...')

        self.__write(request.path, data)

        self._logger.log('Post finalizado com sucesso...')

    def __handle_delete(self, request: Request):
        os.remove('./node/images' + request.path)

    def __create_node_socket(self) -> None:
        new_node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_node_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        new_node_socket.bind(('0.0.0.0', 8010))

        new_node_socket.listen(1)

        while self.__ping_server() != 'PONG':
            print('Not server.')
        else:
            server, _ = new_node_socket.accept()
            self.server_socket = server

    def __ping_server(self) -> str:
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        broadcast_socket.settimeout(200)

        broadcast_socket.sendto('PING'.encode(), ('<broadcast>', 8080))

        data, _ = broadcast_socket.recvfrom(1024)

        return data.decode()
    
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