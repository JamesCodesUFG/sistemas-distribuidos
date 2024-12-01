import rpyc

class GeoEye(rpyc.Service):
    __maestro = rpyc.connect('127.0.0.1', 8081).root

    def __init__(self):
        self.__storage: dict[str, list[str]] = {}
    
    def exposed_get(self, name: str) -> bytes:
        node = self.__maestro.choose(self.__storage[name])

        return node.get(name)

    def exposed_post(self, name: str, file: bytes) -> None:
        _tuples = self.__maestro.next()

        self.__storage[name] = []

        for _tuple in _tuples:
            self.__storage[name].append(_tuple[0])

            _tuple[1].post(name, file)

    def exposed_delete(self, name: str) -> None:
        services = self.__maestro.all(self.__storage[name])

        for service in services:
            service.delete(name)

        del self.__storage[name]

    def exposed_list(self) -> list[str]:
        return list(self.__storage.keys())

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(GeoEye(), port=8080)

    server.start()