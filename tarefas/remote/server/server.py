import rpyc
import math

class GeoEye(rpyc.Service):
    def __init__(self, host: str = 'localhost', port: int = 8090):
        self.__host = host
        self.__port = port

        self.__storage: dict[str, list[str]] = {}
    
    def exposed_get(self, name: str) -> bytes:
        node = self.__connect().choose(self.__storage[name])

        return node.get(name)
    

    def exposed_post(self, name: str, file: bytes) -> None:
        BUFFER_SIZE = 128000

        self.__storage[name] = []

        for inner in range(0, math.ceil(file / BUFFER_SIZE)):
            _tuples = self.__connect().next()

            for node_name, addr in _tuples:
                self.__storage[name].append(node_name)

                conn = rpyc.connect(
                        addr[0], addr[1],
                        config={
                            'allow_pickle': True,
                            'sync_request_timeout': 600
                        })
            
                service = conn.root

                service.post(f'{name}_{inner}', file[inner * BUFFER_SIZE: (inner + 1) * BUFFER_SIZE])


    def exposed_delete(self, name: str) -> None:
        services = self.__connect().all(self.__storage[name])

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

            maestro_addr = rpyc.discover('MAESTRO')[0]

            self.__maestro = rpyc.connect(maestro_addr[0], maestro_addr[1], config={
                    'allow_pickle': True,
                    'sync_request_timeout': 600
                })
        finally:
            return self.__maestro.root
        

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(GeoEye(), port=8080, protocol_config={
        'sync_request_timeout': 600,
        'allow_all_attrs': True,
        'allow_pickle': True,
    })

    print(f'\nGeoEye iniciado em ({server.host, server.port})\n')

    server.start()