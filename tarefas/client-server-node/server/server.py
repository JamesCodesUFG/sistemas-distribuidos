from math import ceil

import socket
from socket import socket as Socket

from threading import Thread

from utils.system import *
from utils.protocol import *
from server.node_handler import NodeHandler

class Server(System):
    __node_handler = NodeHandler(2)
    __storage: dict[str, list[Socket]] = {}

    server_socket: Socket = None
    broadcast_socket: Socket = None

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
        self.server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

        self._logger.log(f'Servidor criado com sucesso...')

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = Socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

        self._logger.log('Broadcast criado com sucesso...')

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = Thread(target=self.__broadcast_loop, daemon=True)

        self.broadcast_thread.start()

    def __broadcast_loop(self):
        
            while True:
                try:
                    response, node_address = self.broadcast_socket.recvfrom(BUFFER_SIZE)

                    self._logger.log(f'{node_address} {response.decode()}')
                
                    if response.decode() == 'PING':
                        self.broadcast_socket.sendto('PONG'.encode(), node_address)

                        new_node = Socket(socket.AF_INET, socket.SOCK_STREAM)

                        new_node.connect(node_address)

                        self.__node_handler.add(new_node)

                        self._logger.log(f'Conexão estabelecida com nó {node_address}...')
                except Exception as error:
                    self._logger.error(error)

    def __handle_client(self, client: Socket):
        request = Request.decode(client.recv(BUFFER_SIZE))

        self._logger.log(f'{client.getpeername()} {request.to_string()}')

        match (request.method):
            case RequestMethod.GET:
                self.__handle_client_get(client, request)
            case RequestMethod.POST:
                self.__handle_client_post(client, request)
            case RequestMethod.DELETE:
                self.__handle_client_delete(client, request)

    def __handle_client_get(self, client: Socket, request: Request):
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
                _node = self.__node_handler.get(request.path[1:])

                _node.send(request.encode())

                response = Response.decode(_node.recv(BUFFER_SIZE))

                self._logger.log(response.to_string())

                data = b''

                for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                    data = data + _node.recv(BUFFER_SIZE)

                client.send(response.encode())

                for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
                    client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

                client.close()

    def __handle_client_post(self, client: Socket, request: Request):
        _nodes = self.__node_handler.next()

        _nodes_name = [element[0] for element in _nodes]
        _nodes_socket = [element[1] for element in _nodes]

        self.__storage[request.path[1:]] = _nodes_name

        data = b''

        client.send(Response(ResponseCode.READY).encode())

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            data = data + client.recv(BUFFER_SIZE)

        for _node in _nodes_socket:
            _node.send(request.encode())

            for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
                _node.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        client.close()

        self._logger.log('Envio finalizado com sucesso...')

    def __handle_client_delete(self, client: Socket, request: Request):
        _nodes = self.__storage[request.path[1:]]

        for _node in _nodes:
            _node.send(request.encode())

SystemManager(Server())