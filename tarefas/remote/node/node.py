import sys
import rpyc
import uuid

from rpyc.utils.server import ThreadedServer

from utils.rabbit import rabbit_send
from utils.file_manager import FileManager

try:
    NODE_NAME = sys.argv[1]
except:
    NODE_NAME = uuid.uuid4()


class NodeService(rpyc.Service):
    ALIASES = [f'NODE_{NODE_NAME}']

    __fmanager: FileManager = FileManager(f'images_{NODE_NAME}')

    def exposed_get(self, name: str) -> bytes:
        file = self.__fmanager.read(name)

        return file

    def exposed_post(self, name: str, file: bytes) -> None:
        self.__fmanager.write(name, file)

    def exposed_delete(self, name: str) -> None:
        self.__fmanager.delete(name)

    def exposed_ping(self) -> str:
        return 'PING'

if __name__ == "__main__":
    import monitor

    __cpu_monitor = monitor.CPUMonitor(0.8, f'NODE_{NODE_NAME}')
    __ram_monitor = monitor.RAMMonitor(0.8, f'NODE_{NODE_NAME}')
    __hdd_monitor = monitor.HDDMonitor(1.0, f'NODE_{NODE_NAME}')

    try:
        __cpu_monitor.start()
        __ram_monitor.start()
        __hdd_monitor.start()

        server = ThreadedServer(NodeService, auto_register=True, protocol_config={
            'sync_request_timeout': 600,
            'allow_all_attrs': True,
            'allow_pickle': True,
            'max_message_size': 10*9,
        })

        rabbit_send('register', f'NODE_{str(NODE_NAME)}')

        print(f'\nNó iniciado em {(server.host, server.port)}\n')

        server.start()
    except:
        __cpu_monitor.stop()
        __ram_monitor.stop()
        __hdd_monitor.stop()
    finally:
        rabbit_send('unregister', f'NODE_{str(NODE_NAME)}')

        
