import rpyc
import uuid
import pprint

from typing import Any

REPLICATION_FACTOR = 2

class Node:
    def __init__(self, port: str, host: int, name: str, dirt: int = 0, ):
        self.name = name
        self.__port = port
        self.__host = host
        self.__dirt = dirt

    def increase(self) -> None:
        self.__dirt += 1

    def decrease(self) -> None:
        if self.__dirt > 0:
            self.__dirt -= 1

    def is_clean(self) -> bool:
        return self.__dirt == 0
    
    def get_address(self) -> tuple:
        return (self.__host, self.__port)
    
    def service(self):
        port = 'localhost' if self.__port == '0.0.0.0' else self.__port

        return rpyc.connect(port, self.__host).root
    
    def copy(self):
        return Node(self.__port, self.__host, self.name, dirt = self.__dirt)

class Maestro(rpyc.Service):
    __current: int = 0

    __nodes: dict[str, Node] = {}

    def exposed_register(self, host: str, port: int) -> None:
        try:
            _name = uuid.uuid4()

            self.__nodes[_name] = (Node(host, port, name=_name))

            print(f'[NODE CONNECTED] ({host, port})\n')
        except Exception as exception:
            print('[ERROR] Tentativa falha de registrar node...\n\n', str(exception))

    def exposed_next(self) -> list[tuple[str, Any]]:
        results: list[Node] = []

        if len(self.__nodes) <= REPLICATION_FACTOR:
            return [(node.name, node.service()) for node in self.__nodes.values()]

        while len(results) < REPLICATION_FACTOR:
            new_node = self.__round_robin()

            if new_node not in results:
                results.append(new_node)

        return [(node.name, node.service()) for node in results]

    def exposed_choose(self, names: list[str]):
        choices = [self.__nodes[name].copy() for name in names]

        result = self.__round_robin_alt(choices)

        return result.service()
    
    def exposed_all(self, names: list[str]):
        result = []

        for name in names:
            node = self.__nodes[name]

            node.increase()

            result.append(node.service())

        return result
    
    def __round_robin(self) -> Node:
        while True:
            _node: Node = list(self.__nodes.values())[self.__current]

            if (_node.is_clean()):
                _node.increase()

                return _node
            
            _node.decrease()

            self.__current = (self.__current + 1) % len(self.__nodes)
    
    def __round_robin_alt(self, nodes: list[Node]) -> Node:
        _current = 0

        while True:
            _node: Node = nodes[_current]

            if (_node.is_clean()):
                self.__nodes[_node.name].increase()

                return _node
            
            _node.decrease()

            _current = (_current + 1) % len(nodes)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(Maestro(), port=8081)

    print(f'Maestro iniciado em ({server.host, server.port})')

    server.start()

    