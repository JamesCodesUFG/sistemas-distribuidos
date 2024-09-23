import socket

class Server:
    def __init__(self, server_ip='0.0.0.0', server_port: int=8080):
        self.server = self.__create_socket((server_ip, server_port))

    def __create_socket(self, server_address: tuple) -> socket:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind(server_address)

        server.listen(4)

        return server