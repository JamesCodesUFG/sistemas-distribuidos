from math import ceil

import socket
from socket import socket as Socket

from threading import Thread

from utils.system import *
from utils.protocol import *
from server.node_manager import NodeManager

class Server(System):
    __node_handler = NodeManager(2)
    __storage: dict[str, list[tuple]] = {}

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
            try:
                client, address = self.server_socket.accept()

                self._logger.log(f'[CLIENT] Cliente: {address[0]}')
            
                Thread(target=self.__handle_client, args=(client, )).start()
            except Exception as error:
                self._logger.error('[CLIENT]', error)

    def exit(self):
        pass
        
    def __create_server_socket(self) -> socket:
        self.server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

        self._logger.log(f'[SERVER] Criado com sucesso...')

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = Socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

        self._logger.log('[BROADCAST] Criado com sucesso...')

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = Thread(target=self.__broadcast_loop, daemon=True)

        self.broadcast_thread.start()

    def __broadcast_loop(self):
            while True:
                try:
                    data, address = self.broadcast_socket.recvfrom(BUFFER_SIZE)
                
                    if data.decode() == 'PING':
                        self.broadcast_socket.sendto('PONG'.encode(), address)

                        self.__node_handler.add(address)

                        self._logger.log(f'[BROADCAST] Nó encontrado: {address}')
                except Exception as error:
                    self._logger.error(error)

    def __handle_client(self, client: Socket):
        try:
            request = Request.decode(client.recv(BUFFER_SIZE))

            self._logger.log(f'[CLIENT REQUEST] {client.getpeername()}, {request}')

            match (request.method):
                case RequestMethod.GET:
                    self.__get(client, request)
                case RequestMethod.LIST:
                    self.__list(client)
                case RequestMethod.POST:
                    self.__post(client, request)
                case RequestMethod.DELETE:
                    self.__delete(client, request)
        except Exception as error:
            self._logger.error(f'[{request.method.name}] {client.getsockname()}, {error}')
        else:
            self._logger.log(f'[{request.method.name}] {client.getsockname()}, sucesso...')
        finally:
            client.close()
            
    def __get(self, client: Socket, request: Request):
        _node = self.__node_handler.get(self.__storage[request.path])

        response = self.__request_node(_node, request)

        client.send(response.encode())

        for inner in range(0, ceil(response.lenght / BUFFER_SIZE)):
            bucket = _node.recv(BUFFER_SIZE)

            client.send(bucket)

    def __list(self, client: Socket):
        _list = [tuple[0] for tuple in self.__storage]

        data = b''

        for name in _list:
            data = data + len(name).to_bytes(1) + name.encode()

        client.send(Response(ResponseCode.OK, len(data)).encode())

        response = Response.decode(client.recv(BUFFER_SIZE))

        if response.status == ResponseCode.READY:
            for inner in range(0, ceil(len(data) / BUFFER_SIZE)):
                client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])
        else:
            raise Exception(f'Não estava pronto...')

    def __post(self, client: Socket, request: Request):
        _nodes = self.__node_handler.next()

        _nodes_names = [element[0] for element in _nodes]
        _nodes_socket = [element[1] for element in _nodes]

        self.__storage[request.path] = _nodes_names

        client.send(Response(ResponseCode.READY).encode())

        for _node in _nodes_socket:
            response = self.__request_node(_node, request)

            if response.status != ResponseCode.READY:
                raise Exception(f'Nó não estava pronto...')

        for inner in range(0, ceil(request.lenght / BUFFER_SIZE)):
            _bucket = client.recv(BUFFER_SIZE)

            for _nodes in _nodes_socket:
                self._logger.log(f'[POST] Enviado para nó: {_node.getsockname()}')

                _node.send(_bucket)

    def __delete(self, client: Socket, request: Request):
        _nodes = self.__node_handler.all(self.__storage[request.path])

        for _node in _nodes:
            _node.send(request.encode())

            response = Response.decode(_node.recv(BUFFER_SIZE))

            self._logger.log(f'[{_node.getsockname()}] {response.status}')

        self.__storage.pop(request.path)

    def __request_node(self, node: Socket, request: Request):
        try:
            node.send(request.encode())

            response = Response.decode(node.recv(BUFFER_SIZE))

            self._logger.log(f'[NODE RESPONSE] {node.getpeername()}, {response}')

            return response
        except Exception as error:
            raise Exception(f'Erro na requisição para o nó...')

SystemManager(Server())