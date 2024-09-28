import socket

from threading import Thread

from utils.protocol import *

class Server:
    node_socket: socket.socket = None
    server_socket: socket.socket = None
    broadcast_socket: socket.socket = None

    server_thread: Thread = None
    broadcast_thread: Thread = None

    def __init__(self, server_ip='0.0.0.0', server_port: int=8080):
        self.server_address = (server_ip, server_port)

        self.__create_server_socket()
        self.__create_broadcast_socket()

        self.__start_server_thread()
        self.__start_broadcast_thread()
        
    def __create_server_socket(self) -> socket:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(4)

    def __create_broadcast_socket(self) -> None:
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast_socket.bind(('0.0.0.0', 8080))

    def __start_server_thread(self):
        self.broadcast_thread = Thread(target=self.__server_loop)

        self.broadcast_thread.start()

    def __start_broadcast_thread(self) -> None:
        self.broadcast_thread = Thread(target=self.__broadcast_loop)

        self.broadcast_thread.start()

    def __server_loop(self):
        while True:
            client, _ = self.server_socket.accept()
            
            Thread(target=self.__handle_client, args=(client, )).start()

    def __broadcast_loop(self):
        while True:
            response, node_address = self.broadcast_socket.recvfrom(BUFFER_SIZE)

            print(node_address)
            
            if response.decode() == 'PING':
                self.broadcast_socket.sendto('PONG'.encode(), node_address)

                self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                self.node_socket.connect(node_address)

    def __handle_client(self, client: socket.socket):
        request = Request.decode(client.recv(BUFFER_SIZE))

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
                # TODO: Retornar uma lista com nome das imagens inseridas.

                client.send(Response(ResponseCode.BAD_REQUEST).encode())

                client.close()
            case _:
                self.node_socket.send(request.encode())

                response = Response.decode(self.node_socket.recv(BUFFER_SIZE))

                data = b''

                for inner in range(0, response.lenght // BUFFER_SIZE):
                    data = data + self.node_socket.recv(BUFFER_SIZE)

                client.send(response.encode())

                for inner in range(0, response.lenght // BUFFER_SIZE):
                    client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

                client.close()

    def __handle_client_post(self, client: socket.socket, request: Request):
        path = request.path.split('/')[1:]

        self.node_socket.send(request.encode())

        response = Response.decode(self.node_socket.recv(BUFFER_SIZE))

        data = b''

        for inner in range(0, response.lenght // BUFFER_SIZE):
            data = data + self.node_socket.recv(BUFFER_SIZE)

        client.send(Response(ResponseCode.OK, len(data)).encode())

        for inner in range(0, response.lenght // BUFFER_SIZE):
            client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

        client.close()

    def __handle_client_delete(client: socket.socket, request: Request):
        pass

    def __handle_node():
        pass

server = Server()