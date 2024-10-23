from math import ceil

import socket
from socket import socket as Socket

from utils.logger import *
from utils.protocol import *
from utils.file_manager import *

class Client:
    __file: FileManager = FileManager(r'C:\Users\tiago\Documents\Workflows\UFG\sistemas-distribuidos\tarefas\client-server-node\client\images')

    def __init__(self, server_ip: str, server_port: int = 8080):
        self.server_address = (server_ip, server_port)

    def get(self, path:str):
        client: Socket = self.__create_socket()

        response = self.__request(client, Request(RequestMethod.GET, path))

        data = b''

        if response.status == ResponseCode.OK:
            for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                data = data + client.recv(BUFFER_SIZE)

            self.__file.write(path, data)
        else:
            print(f'ERROR: {response.status}')

        client.close()

    def list(self, path:str='/') -> list[str]:
        client: Socket = self.__create_socket()

        response = self.__request(client, Request(RequestMethod.LIST, path))

        client.send(Response(ResponseCode.READY).encode())

        data = b''

        if response.status == ResponseCode.OK:
            for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                data = data + client.recv(BUFFER_SIZE)

            files = []

            bytes_read = 0

            while bytes_read < response.lenght:
                string_lenght = int.from_bytes(data[bytes_read:bytes_read + 1])

                index_start = bytes_read + 1
                index_end = index_start + string_lenght

                files.append(data[index_start: index_end].decode())

                bytes_read = bytes_read + string_lenght + 1

            print(files)
        else:
            print(f'ERROR: {response.status}')

        client.close()

    def post(self, path: str) -> Socket:
        client: Socket = self.__create_socket()

        data = self.__file.read(path)

        response = self.__request(client, Request(RequestMethod.POST, path, len(data)))

        if response.status == ResponseCode.READY:
            for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
                client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        client.close()

    def delete(self, path: str) -> None:
        client: Socket = self.__create_socket()

        request = Request(RequestMethod.DELETE, path)

        client.send(request.encode())

        client.close()

    def __create_socket(self: tuple) -> socket:
        client = Socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(self.server_address)

        return client

    def __request(self, client: Socket, request: Request) -> Response:
        client.send(request.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        return response

client = Client('127.0.0.1')

#client.post('a.jpg')
#client.get('a.jpg')
#client.list()
client.delete('a.jpg')

#client.post('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND1.tif')
#client.get('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND1.tif')
#client.get('/all')
#client.delete('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND1.tif')