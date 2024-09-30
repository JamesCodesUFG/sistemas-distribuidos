import socket

from utils.protocol import *

class Node:
    server_socket: socket.socket = None

    def __init__(self):
        self.__create_node_socket()

        self.__main_loop()

    def __main_loop(self):
        for inner in range(0, 2):
            request = Request.decode(self.server_socket.recv(BUFFER_SIZE))

            print(f'Request: {request.method.name} -> {request.path}', request.lenght)

            match request.method:
                case RequestMethod.GET:
                    self.__handle_get(request)
                case RequestMethod.POST:
                    self.__handle_post(request)
                case RequestMethod.DELETE:
                    self.__handle_delete(request)

    def __handle_get(self, request: Request):
        data = self.__read(request.path[1:])

        self.server_socket.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, len(data) // BUFFER_SIZE):
            self.server_socket.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    def __handle_post(self, request: Request):
        data = b''

        for inner in range(0, request.lenght // BUFFER_SIZE):
            print('----> Recebendo dados: {inner}.')
            data = data + self.server_socket.recv(BUFFER_SIZE)

        self.__write(request.path[1:], data)

    def __handle_delete(self, request: Request):
        pass

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

        broadcast_socket.bind(('0.0.0.0', 8010))

        broadcast_socket.settimeout(200)

        broadcast_socket.sendto('PING'.encode(), ('<broadcast>', 8080))

        data, _ = broadcast_socket.recvfrom(1024)

        return data.decode()
    
    def __read(self, file_name: str) -> bytes:
        data: bytes = None

        with open('./node/' + file_name, 'rb') as file:
            data = file.read()

        return data

    def __write(self, file_name: str, data: bytes) -> None:
        with open('./node/' + file_name, 'wb') as file:
            file.write(data)
    
node = Node()