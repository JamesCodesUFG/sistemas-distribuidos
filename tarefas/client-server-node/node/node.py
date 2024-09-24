import socket

class Node:
    node_socket: socket = None

    def __init__(self):
        server_address = self.__find_server_address()

        self.__connect_to_server(server_address)

    def __connect_to_server(self, server_address: tuple) -> None:
        self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.node_socket.connect(server_address)

    def __find_server_address(self) -> tuple:
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        broadcast_socket.sendto('PING'.encode(), ('<broadcast>', 8080))

        while True:
            response, address = broadcast_socket.recvfrom(1024)

            if response.decode() == 'PONG':
                return address
    
node = Node()