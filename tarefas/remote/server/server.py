import rpyc
import math

from utils.rabbit import rabbit_multiple_send

class GeoEye(rpyc.Service):
    def __init__(self):
        self.__storage: dict[str, dict[str, str]] = {}
    
    def exposed_get(self, name: str, shard: int) -> bytes:
        result = b''

        port, host = self.__connect_maestro().get(self.__storage[name][shard])

        service = self.__connect_node(port, host)

        result += service.get(f'{name}_{shard}')

        return result
    

    def exposed_post(self, file_name: str, part: int, file: bytes) -> None:
        if not file_name in self.__storage:
            self.__storage[file_name] = {}

        node_name = self.__connect_maestro().next()

        self.__storage[file_name][part] = node_name

        message = {
            'name': f'{file_name}_{part}',
            'file': file
        }

        rabbit_multiple_send(f'post_{node_name}', message)


    def exposed_delete(self, name: str) -> None:
        for key in self.__storage[name]:
            rabbit_multiple_send(f'delete_{self.__storage[name][key]}', { 'name': f'{name}_{key}'})

        del self.__storage[name]


    def exposed_list(self) -> list[str]:
        return list(self.__storage.keys())
    
    def exposed_chunck_lenght(self, file_name: str) -> int:
        return len(self.__storage[file_name])
    
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