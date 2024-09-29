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

        self.__write(path[1:], data)

    def post(self, path: str) -> socket.socket:
        client: socket.socket = self.__create_socket()

        data = self.__read(path[1:])

        request = Request(RequestMethod.POST, path, len(data))

        client.send(request.encode())

        for inner in range(0, len(data) // BUFFER_SIZE):
            client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    def delete(self, path: str) -> None:
        request = Request(RequestMethod.DELETE, path)

    def __create_socket(self: tuple) -> socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(self.server_address)

        return client

    def __read(self, file_name: str) -> bytes:
        data: bytes = None

        with open('./client/' + file_name, 'rb') as file:
            data = file.read()

        return data

    def __write(self, file_name: str, data: bytes) -> None:
        with open('./client/' + file_name, 'wb') as file:
            file.write(data)
    
Client('192.168.56.1').get('/a.jpg')