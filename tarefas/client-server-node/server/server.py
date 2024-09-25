from socket import socket

from threading import Thread

BUFFER_SIZE = 1024

class Server:
    server_socket: socket = None
    broadcast_socket: socket = None

    server_thread: Thread = None
    broadcast_thread: Thread = None

    def __init__(self, server_ip='0.0.0.0', server_port: int=8080):
        self.server_address = (server_ip, server_port)

        self.__create_server_socket()
        self.__create_broadcast_socket()

        self.__start_broadcast_thread()

    def __main__(self):
        while True:
            client, _ = self.server_socket.accept()

            self.__start_client_thread(client)

    def __create_server_socket(self) -> socket:
        self.server_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

    def __start_client_thread(self, client: socket) -> None:
        self.server_thread = Thread(target=self.__handle_client(), args=(client,))

        self.server_thread.start()

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = Thread(target=self.__listen_to_ping())

        self.broadcast_thread.start()

    def __handle_client(client: socket):
        request = client.recv(BUFFER_SIZE).decode()

        method, 

    def __handle_node():
        pass

    def __listen_to_ping(self):
        while True:
            response, node_address = self.broadcast_socket.recvfrom(1024)
            
            if response.decode() == 'PING':
                self.broadcast_socket.sendto('PONG'.encode(), node_address)

server = Server()