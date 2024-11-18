import rpyc

from server.node_manager import Node, NodeManager

REPLICATION_FACTOR = 1

class GeoEye(rpyc.Service):
    __node_manager: NodeManager = NodeManager(REPLICATION_FACTOR)

    def __init__(self):
        self.storage: dict[str, list[Node]] = {}

    def exposed_get(self, name: str) -> bytes:
        service = self.__node_manager.get(self.storage[name])

        return service.get(name)

    def exposed_post(self, name: str, file: bytes) -> None:
        _tuples = self.__node_manager.next()

        self.storage[name] = []

        for _tuple in _tuples:
            self.storage[name].append(_tuple[0])

            _tuple[1].post(name, file)

    def exposed_delete(self, name: str) -> None:
        services = self.__node_manager.all(self.storage[name])

        for service in services:
            service.delete(name)

        del self.storage[name]

    def exposed_list(self) -> list[str]:
        return list(self.storage.keys())

    def exposed_register(self, host: str, port: int) -> None:
        self.__node_manager.add(host, port)

        print(host, port)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(GeoEye(), port=8080)

    server.start()