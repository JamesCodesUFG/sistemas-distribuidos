import socket

from utils.protocol import *

class Client:
    def __init__(self, server_ip: str, server_port: int = 8080):
        self.server_address = (server_ip, server_port)

    def get(self, path: str):
        client: socket.socket = self.__create_socket()

        request = Request(RequestMethod.GET, path)

        client.send(request.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        data = b''

        # TODO: Implementar como match.
        if response.status == ResponseCode.OK:
            for inner in range(0, response.lenght // BUFFER_SIZE):
                data = data + client.recv(BUFFER_SIZE)
        else:
            print(f'ERROR: {response.status}')

        return data.decode()

    def post(self, name: str) -> socket.socket:
        client: socket.socket = self.__create_socket()

        client.send(f'GET {name}'.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        data = b''

        # TODO: Implementar como match.
        if response.status == ResponseCode.OK:
            for inner in range(0, response.lenght // BUFFER_SIZE):
                data = data + client.recv(BUFFER_SIZE)
        else:
            print(f'ERROR: {response.status}')

        # TODO: Salvar a imagem localmente.

        return data.decode()

    def __create_socket(self: tuple) -> socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(self.server_address)

        return client
    
Client('192.168.0.13').get('/all')