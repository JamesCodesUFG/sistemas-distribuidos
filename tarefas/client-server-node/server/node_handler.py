from socket import socket as Socket

class NodeHandler():
    PREFIX = 'NODE-0'

    __size: int = 0
    __current: int = 0

    __nodes: dict = {}

    def __init__(self, replication_factor: int):
        self.__replication_factor = replication_factor

    def add(self, node: Socket):
        self.__nodes[f'{self.PREFIX}{self.__size + 1}'] = node

    def get(self, name: str) -> Socket:
        return self.__nodes[name]

    def next(self) -> list[tuple[str, Socket]]:
        return [self.__nodes[self.__round_robin()] for i in range(0, self.__replication_factor)]
    
    def __round_robin(self) -> str:
        self.__current = (self.__current + 1) % self.__size

        return f'{self.PREFIX}{self.__current}'


        