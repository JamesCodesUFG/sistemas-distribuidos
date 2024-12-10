import rpyc
import math

class GeoEye(rpyc.Service):
    def __init__(self):
        self.__storage: dict[str, dict[str, list[str]]] = {}
    
    def exposed_get(self, name: str) -> bytes:
        result = b''

        for key in self.__storage[name]:
            port, host = self.__connect_maestro().choose(self.__storage[name][key])

            service = self.__connect_node(port, host)

            result += service.get(f'{name}_{key}')

        return result
    

    def exposed_post(self, name: str, file: bytes) -> None:
        BUFFER_SIZE = 540672

        self.__storage[name] = {}

        for inner in range(0, math.ceil(len(file) / BUFFER_SIZE)):
            self.__storage[name][inner] = []

            _tuples = self.__connect_maestro().next()

            for node_name, addr in _tuples:
                self.__storage[name][inner].append(node_name)

                service = self.__connect_node(addr[0], addr[1])

                service.post(f'{name}_{inner}', file[inner * BUFFER_SIZE: (inner + 1) * BUFFER_SIZE])


    def exposed_delete(self, name: str) -> None:
        for key in self.__storage[name]:
            _addrs = self.__connect_maestro().all(self.__storage[name][key])

            for host, port in _addrs:
                service = self.__connect_node(host, port)

                service.delete(f'{name}_{key}')

        del self.__storage[name]


    def exposed_list(self) -> list[str]:
        return list(self.__storage.keys())
    
    
    def __connect_node(self, host: str, port: str):
        return rpyc.connect(
                        host, port,
                        config={
                            'allow_pickle': True,
                            'sync_request_timeout': None
                        }).root
    
    
    def __connect_maestro(self):
        try:
            self.__maestro.ping()
        except:
            print(f'\n[WARNING] Restabelecendo conexão com servidor...')

            maestro_addr = rpyc.discover('MAESTRO')[0]

            self.__maestro = rpyc.connect(maestro_addr[0], maestro_addr[1], config={
                    'allow_pickle': True,
                    'sync_request_timeout': None
                })
        finally:
            return self.__maestro.root
        

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(GeoEye(), port=8080, protocol_config={
        'sync_request_timeout': None,
        'allow_all_attrs': True,
        'allow_pickle': True,
    })

    print(f'\nGeoEye iniciado em ({server.host, server.port})\n')

    server.start()