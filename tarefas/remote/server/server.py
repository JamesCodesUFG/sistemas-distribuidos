import rpyc

class GeoEye(rpyc.Service):
    def __init__(self, host: str = 'localhost', port: int = 8090):
        self.__host = host
        self.__port = port

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
    
    def __connect(self):
        try:
            self.__maestro.ping()
        except:
            print(f'\n[WARNING] Restabelecendo conexão com servidor...')

            self.__maestro = rpyc.connect(self.__host, self.__port)
        finally:
            return self.__maestro.root

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(GeoEye(), port=8080)

    server.start()