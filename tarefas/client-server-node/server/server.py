from math import ceil
import socket

from threading import Thread

from utils.system import *
from utils.protocol import *
from node_handler import NodeHandler

class Server(System):
    __node_handler = NodeHandler
    storage: list[tuple] = []

    node_socket: socket.socket = None
    server_socket: socket.socket = None
    broadcast_socket: socket.socket = None

    server_thread: Thread = None
    broadcast_thread: Thread = None

    def __init__(self, server_ip='0.0.0.0', server_port: int=8080):
        super().__init__()

        self.daemon = True

        self.server_address = (server_ip, server_port)

        self.__create_server_socket()
        self.__create_broadcast_socket()

        self.__start_broadcast_thread()

    def run(self):
        while True:
            client, address = self.server_socket.accept()

            self._logger.log(f'Conexão estabelecida com {address[0]}.')
            
            Thread(target=self.__handle_client, args=(client, )).start()

    def exit(self):
        pass
        
    def __create_server_socket(self) -> socket:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

        self._logger.log(f'Servidor criado com sucesso...')

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

        self._logger.log('Broadcast criado com sucesso...')

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = Thread(target=self.__broadcast_loop, daemon=True)

        self.broadcast_thread.start()

    def __broadcast_loop(self):
        while True:
            response, node_address = self.broadcast_socket.recvfrom(BUFFER_SIZE)

            self._logger.log(f'{node_address} {response.decode()}')
            
            if response.decode() == 'PING':
                self.broadcast_socket.sendto('PONG'.encode(), node_address)

                self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.node_socket.connect(node_address)

                self._logger.log(f'Conexão estabelecida com nó {node_address}...')

    def __handle_client(self, client: socket.socket):
        request = Request.decode(client.recv(BUFFER_SIZE))

        self._logger.log(f'{client.getpeername()} {request.to_string()}')

        match (request.method):
            case RequestMethod.GET:
                self.__handle_client_get(client, request)
            case RequestMethod.POST:
                self.__handle_client_post(client, request)
            case RequestMethod.DELETE:
                self.__handle_client_delete(client, request)

    def __handle_client_get(self, client: socket.socket, request: Request):
        path = request.path.split('/')[1:]

        match (path[0]):
            case 'all':
                file_list = [tuple[0] for tuple in self.storage]

                data = b''

                for file_name in file_list:
                    data = data + len(file_name).to_bytes(1) + file_name.encode()

                client.send(Response(ResponseCode.OK, len(data)).encode())

                response = Response.decode(client.recv(BUFFER_SIZE))

                if response.status == ResponseCode.READY:
                    for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
                        client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])
                else:
                    self._logger.error(f'Client {client.getpeername()} not ready...')

                client.close()
            case _:
                self.node_socket.send(request.encode())

                response = Response.decode(self.node_socket.recv(BUFFER_SIZE))

                self._logger.log(response.to_string())

                data = b''

                for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                    data = data + self.node_socket.recv(BUFFER_SIZE)

                client.send(response.encode())

                for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                    client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

                client.close()

    def __handle_client_post(self, client: socket.socket, request: Request):
        self.storage.append((request.path[1:], self.node_socket))

        data = b''

        client.send(Response(ResponseCode.READY).encode())

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            data = data + client.recv(BUFFER_SIZE)

        client.close()

        self.node_socket.send(request.encode())

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            self.node_socket.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        self._logger.log('Envio finalizado com sucesso...')

    def __handle_client_delete(self, client: socket.socket, request: Request):
        self.node_socket.send(request.encode())

    def __handle_node():
        pass

SystemManager(Server())