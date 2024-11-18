import rpyc
import random

class Node:
    def __init__(self, port: str, host: int):
        self.__port = port
        self.__host = host
        self.__dirt_bit = 0

    def increase(self) -> None:
        self.__dirt_bit += 1

    def decrease(self) -> None:
        if self.__dirt_bit > 0:
            self.__dirt_bit -= 1

    def is_clean(self) -> bool:
        return self.__dirt_bit == 0
    
    def get_address(self) -> tuple:
        return (self.__host, self.__port)
    
    def service(self):
        port = 'localhost' if self.__port == '0.0.0.0' else self.__port

        return rpyc.connect(port, self.__host).root

class NodeManager():
    __current: int = 0

    __nodes: list[Node] = []

    def __init__(self, factor: int):
        self.replication_factor = factor

    def add(self, host: str, port: int):
        self.__nodes.append(Node(host, port))

    def get(self, nodes: list[Node]):
        node = random.choice(nodes)

        node.increase()

        return node.service()
    
    def all(self, nodes: list[Node]):
        services = []

        for node in nodes:
            node.increase()

            services.append(node.service())

        return services

    def next(self):
        nodes = []

        if len(self.__nodes) <= self.replication_factor:
            nodes = self.__nodes
        else:
            while len(nodes) < self.replication_factor:
                node = self.__round_robin()

                if node not in nodes:
                    nodes.append(node)

        return [(node, node.service()) for node in nodes]
    
    def __round_robin(self) -> Node:
        while True:
            if (self.__nodes[self.__current].is_clean()):
                self.__nodes[self.__current].increase()

                return self.__nodes[self.__current]
            
            self.__nodes[self.__current].decrease()

            self.__current = (self.__current + 1) % len(self.__nodes)
    
