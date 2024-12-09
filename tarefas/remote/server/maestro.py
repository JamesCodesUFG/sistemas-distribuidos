import rpyc

from typing import Any

from utils.rabbit import RabbitReceiver

REPLICATION_FACTOR = 2

current_index: int = 0

maestro_nodes: dict[str, 'Node'] = {}

def __register_node(name: bytes):
    global maestro_nodes

    maestro_nodes[name.decode()] = Node(name.decode())

def __unregister_node(body: bytes):
    global maestro_nodes

    del maestro_nodes[body.decode()]

def __monitor_node(body: bytes):
    name, type, status = body.decode().split(' ')

    print(f'Node: {name[:4]}, Tipo: {type}, Status: {status}')

rabbit_register = RabbitReceiver('register', __register_node)
rabbit_unregister = RabbitReceiver('unregister', __unregister_node)
rabbit_monitor = RabbitReceiver('monitor', __monitor_node)

rabbit_register.start()
rabbit_unregister.start()
rabbit_monitor.start()

class Node:
    def __init__(self, name: str, dirt: int = 0):
        self.name = name
        self.__dirt = dirt

    def increase(self) -> None:
        self.__dirt += 1

    def decrease(self) -> None:
        if self.__dirt > 0:
            self.__dirt -= 1

    def is_chooseable(self) -> bool:
        return self.__dirt == 0
    
    def addr(self):
        host, port = rpyc.discover(self.name)[0]

        return (host, port)
    
    def copy(self):
        return Node(self.name, self.__dirt)

class MaestroService(rpyc.Service):
    ALIASES = ['MAESTRO']
    
    def __init__(self) -> None:
        super().__init__()

        self.__discover_nodes()


    def exposed_next(self) -> list[tuple[str, Any]]:
        global maestro_nodes

        results: list[Node] = []

        if len(maestro_nodes) <= REPLICATION_FACTOR:
            return [(node.name, node.addr()) for node in maestro_nodes.values()]

        while len(results) < REPLICATION_FACTOR:
            new_node = self.__round_robin()

            if new_node not in results:
                results.append(new_node)

        services = [(node.name, node.addr()) for node in results]

        return services
    

    def exposed_choose(self, names: list[str]):
        global maestro_nodes

        choices = [maestro_nodes[name].copy() for name in names]

        result = self.__round_robin_alt(choices)

        return result.addr()
    
    def exposed_all(self, names: list[str]):
        global maestro_nodes

        result = []

        for name in names:
            node = maestro_nodes[name]

            node.increase()

            result.append(node.addr())

        return result
    
    
    def __round_robin(self) -> Node:
        global maestro_nodes
        global current_index

        while True:
            _node: Node = list(maestro_nodes.values())[current_index]

            if (_node.is_chooseable()):
                _node.increase()

                return _node
            
            _node.decrease()

            current_index = (current_index + 1) % len(maestro_nodes)

    
    def __round_robin_alt(self, nodes: list[Node]) -> Node:
        global maestro_nodes

        _current = 0

        while True:
            _node: Node = nodes[_current]

            if (_node.is_chooseable()):
                maestro_nodes[_node.name].increase()

                return _node
            
            _node.decrease()

            _current = (_current + 1) % len(nodes)


    def __discover_nodes(self):
        global maestro_nodes

        try:
            services = rpyc.list_services()

            for name in services:
                if (not name[:4] == 'NODE'):
                    continue

                maestro_nodes[name] = Node(name)
        except rpyc.utils.factory.DiscoveryError:
            print('No nodes were found...')


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(MaestroService(), port=8090, auto_register=True, protocol_config={
        'sync_request_timeout': 600,
        'allow_all_attrs': True,
        'allow_pickle': True,
    })

    print(f'\nMaestro iniciado em ({server.host, server.port})\n')

    server.start()

    