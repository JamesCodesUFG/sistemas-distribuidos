import socket

from ..utils.protocol import *

class Client:
    def __init__(self, server_ip: str, server_port: int):
        self.server_address = (server_ip, server_port)

    def get(self, path: str):
        client: socket.socket = self.__create_socket(self.server_address)

        request = Request(RequestMethod.GET, path, 0)

        client.send(request.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        data = b''

        if response[0] == 'OK':
            for inner in range(0, response[1] / BUFFER_SIZE):
                data = data + client.recv(BUFFER_SIZE)
        else:
            print(f'ERROR: {response[1]}')

        # Salvar a imagem localmente.

        return data.decode()

    def list(self, name: str):
        pass

    def post(self, name: str) -> socket.socket:
        client = self.__create_socket(self.server_address)

        client.send(f'GET {name}'.encode())

        response: bytes = client.recv(BUFFER_SIZE).decode()

        data = b''

        if response[0] == 'OK':
            for inner in range(0, response[1] / BUFFER_SIZE):
                data = data + client.recv(BUFFER_SIZE)
        else:
            print(f'ERROR: {response[1]}')

        # Salvar a imagem localmente.

        return data.decode()

    def __create_socket(server_address: tuple) -> socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(server_address)

        return client