import socket

from utils.protocol import *

class Node:
    server_socket: socket.socket = None

    def __init__(self):
        self.__create_node_socket()

        self.__main_loop()

    def __main_loop(self):
        for inner in range(0, 1):
            request = Request.decode(self.server_socket.recv(BUFFER_SIZE))

            print(request.method, request.path, request.lenght)

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

        broadcast_socket.settimeout(2)

        broadcast_socket.sendto('PING'.encode(), ('<broadcast>', 8080))

        data, _ = broadcast_socket.recvfrom(1024)

        return data.decode()
    
node = Node()