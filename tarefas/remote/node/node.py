import rpyc
import uuid

from utils.file_manager import FileManager

SERVER_HOST = 'localhost'

def register_to_server(host: str, port: int) -> None:
    maestro = rpyc.connect(SERVER_HOST, 8090).root

    maestro.register(host, port)

class NodeService(rpyc.Service):
    ALIASES = [f'{uuid.uuid4()}']

    __file_manager: FileManager = FileManager(f'images_{ALIASES[0]}')

    def exposed_get(self, name: str) -> bytes:
        file = self.__file_manager.read(name)

        return file

    def exposed_post(self, name: str, file: bytes) -> None:
        self.__file_manager.write(name, file)

    def exposed_delete(self, name: str) -> None:
        self.__file_manager.delete(name)

    def exposed_ping(self) -> str:
        return 'PING'

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    server = ThreadedServer(NodeService)

    print(f'Nó iniciado em {(server.host, server.port)}')

    register_to_server(server.host, server.port)

    server.start()