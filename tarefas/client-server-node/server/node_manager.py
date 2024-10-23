import socket
from socket import socket as Socket

class NodeManager():
    __size: int = 0
    __current: int = 0

    __nodes: list[tuple] = []

    def __init__(self, replication_factor: int):
        self.__replication_factor = replication_factor

    def add(self, address: tuple):
        self.__size += 1
        self.__nodes.append(address)

    def get(self, addresses: list[tuple]) -> Socket:
        return self.__connect(addresses[0])
    
    def all(self, addresses: list[tuple]) -> list[Socket]:
        return [self.__connect(address) for address in addresses]

    def next(self) -> set[tuple[tuple, Socket]]:
        _nodes = set([self.__nodes[self.__round_robin()] for i in range(0, self.__replication_factor)])

        return [(_node, self.__connect(_node)) for _node in _nodes]
    
    def __connect(self, address: tuple):
        new_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)

        new_socket.connect(address)

        return new_socket
    
    def __round_robin(self) -> int:
        self.__current = (self.__current + 1) % self.__size

        return self.__current

class Node:
    pass
        