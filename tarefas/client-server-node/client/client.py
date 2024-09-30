from math import ceil
import socket

from utils.protocol import *
from utils.logger import *

class Client:
    def __init__(self, server_ip: str, server_port: int = 8080):
        self.server_address = (server_ip, server_port)

    def get(self, path: str):
        client: socket.socket = self.__create_socket()

        request = Request(RequestMethod.GET, path)

        client.send(request.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        match path[1:]:
            case 'all':
                data = b''

                client.send(Response(ResponseCode.READY).encode())

                if response.status == ResponseCode.OK:
                    for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                        data = data + client.recv(BUFFER_SIZE)

                    print(data)

                    files = []

                    bytes_read = 0

                    while bytes_read < response.lenght:
                        string_lenght = int.from_bytes(data[bytes_read:bytes_read + 4])

                        index_start = bytes_read + 1
                        index_end = bytes_read + string_lenght + 2

                        files.append(data[index_start: index_end].decode())

                        bytes_read = bytes_read + string_lenght + 1

                    print(files)
                else:
                    print(f'ERROR: {response.status}')

            case _:
                data = b''

                if response.status == ResponseCode.OK:
                    for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                        data = data + client.recv(BUFFER_SIZE)
                else:
                    print(f'ERROR: {response.status}')

                self.__write(path, data)

        client.close()

    def post(self, path: str) -> socket.socket:
        client: socket.socket = self.__create_socket()

        data = self.__read(path)

        request = Request(RequestMethod.POST, path, len(data))

        client.send(request.encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        if response.status == ResponseCode.READY:
            for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
                client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        client.close()

    def delete(self, path: str) -> None:
        request = Request(RequestMethod.DELETE, path)

    def __create_socket(self: tuple) -> socket:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect(self.server_address)

        return client

    def __read(self, file_name: str) -> bytes:
        data: bytes = None

        with open('./client/images' + file_name, 'rb') as file:
            data = file.read()

        return data

    def __write(self, file_name: str, data: bytes) -> None:
        with open('./client/images' + file_name, 'wb') as file:
            file.write(data)

client = Client('172.16.55.155')

client.post('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND1.tif')
#client.get('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND4.tif')
#client.get('/all')
#client.delete('/AMAZONIA_1_WFI_20240909_036_018_L4_BAND1.tif')