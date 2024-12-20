import rpyc

from typing import Any

from utils.rabbit import *

REPLICATION_FACTOR = 2

current_index: int = 0

maestro_nodes: dict[str, 'Node'] = {}


def __register_node(data: dict):
    global maestro_nodes

    if not data['name'] in maestro_nodes:
        maestro_nodes[data['name']] = Node(data['name'])

        print('Nó regsitrado com sucesso...')
    else:
        host, port = maestro_nodes[data['name']].addr()

        service = rpyc.connect(host, port, config={
                    'allow_pickle': True,
                    'sync_request_timeout': None
                }).root

        service.sync()
        
        print('Nó já foi regsitrado...')


def __monitor_node(data: dict):
    global maestro_nodes

    name = data['name']
    comp = data['comp']
    status = data['status']

    try:
        if data['status'] == 'HEAT':
            maestro_nodes[data['node']].lock()
        elif data['status'] == 'COLD':
            maestro_nodes[data['node']].unlock()

        print(f'Node: {name}, Tipo: {comp}, Status: {status}')
    except:
        print('Tentativa falha de monitoramento...')
    

rabbit_register = RabbitSingleReceiver('register', __register_node)
rabbit_monitor = RabbitSingleReceiver('monitor', __monitor_node)

rabbit_register.start()
rabbit_monitor.start()

class Node:
    def __init__(self, name: str, dirt: int = 0, lock: bool = False):
        self.name = name
        self.__dirt = dirt
        self.__lock = lock

    def increase(self) -> None:
        self.__dirt += 1

    def decrease(self) -> None:
        if self.__dirt > 0:
            self.__dirt -= 1

    def lock(self) -> None:
        self.__lock = True

    def unlock(self) -> None:
        self.__lock = False

    def is_chooseable(self) -> bool:
        return self.__dirt == 0
    
    def is_unlocked(self) -> bool:
        return not self.__lock
    
    def addr(self):
        host, port = rpyc.discover(self.name)[0]

        return (host, port)
    
    def copy(self):
        return Node(self.name, self.__dirt, self.__lock)

class MaestroService(rpyc.Service):
    ALIASES = ['MAESTRO']
    
    def __init__(self) -> None:
        super().__init__()

        self.__discover_nodes()


    def exposed_next(self) -> list[tuple[str, Any]]:
        global maestro_nodes

        return self.__round_robin().name
    

    def exposed_get(self, name: str):
        global maestro_nodes

        return maestro_nodes[name].addr()
    
    
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

            if (_node.is_chooseable() and _node.is_unlocked()):
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

    