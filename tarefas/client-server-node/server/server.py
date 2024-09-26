import socket

import threading

from ..utils.protocol import *

class Server:
    server_socket: socket.socket = None
    broadcast_socket: socket.socket = None

    server_thread: threading = None
    broadcast_thread: threading = None

    def __init__(self, server_ip='0.0.0.0', server_port: int=8080):
        self.server_address = (server_ip, server_port)

        self.__create_server_socket()
        self.__create_broadcast_socket()

        self.__start_server_thread()
        self.__start_broadcast_thread()
        
    def __create_server_socket(self) -> socket:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

    def __start_server_thread(self): 
        self.broadcast_thread = threading.Thread(target=self.__server_loop())

        self.broadcast_thread.start()

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = threading.Thread(target=self.__broadcast_loop())

        self.broadcast_thread.start()

    def __server_loop(self):
        while True:
            client, _ = self.server_socket.accept()
            
            threading.Thread(target=self.__handle_client(), args=(client, )).start()

    def __broadcast_loop(self):
        while True:
            response, node_address = self.broadcast_socket.recvfrom(1024)
            
            if response.decode() == 'PING':
                self.broadcast_socket.sendto('PONG'.encode(), node_address)

    def __handle_client(self, client: socket.socket):
        request = Request.decode(client.recv(1024))

        match (request.method):
            case RequestMethod.GET:
                self.__handle_client_get(client, request)
            case RequestMethod.POST:
                self.__handle_client_post(client, request)
            case RequestMethod.DELETE:
                self.__handle_client_delete(client, request)

    def __handle_client_get(client: socket.socket, request: Request):
        path = request.path.split('/')[1:]

        match (request.path[0]):
            case 'list':
                pass
            case _:
                pass

    def __handle_client_post(client: socket.socket, request: Request):
        pass

    def __handle_client_delete(client: socket.socket, request: Request):
        pass

    def __handle_node():
        pass

server = Server()