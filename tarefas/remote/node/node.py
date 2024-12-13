import sys
import rpyc
import uuid
import json

from rpyc.utils.server import ThreadedServer

from utils.rabbit import *
from utils.file_manager import FileManager

NODE_NAME = sys.argv[1]

fmanager: FileManager = FileManager(f'images_{NODE_NAME}')

def post(body: bytes):
    global fmanager

    data = json.loads(body)

    fmanager.write(data['name'], data['file'])


def delete(body: bytes):
    global fmanager

    data = json.loads(body)

    fmanager.delete(data['name'])

rabbit_post = RabbitMultipleReceiver(sys.argv[2], f'post_{NODE_NAME}', post)
rabbit_delete = RabbitMultipleReceiver(sys.argv[2], f'delete_{NODE_NAME}', delete)

class NodeService(rpyc.Service):
    ALIASES = [f'NODE_{NODE_NAME}']

    def exposed_get(self, name: str) -> bytes:
        file = self.__fmanager.read(name)

        return file


if __name__ == "__main__":
    import monitor

    __hdd_monitor = monitor.HDDMonitor(0.9, f'NODE_{NODE_NAME}')

    try:
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
        __hdd_monitor.stop()
    finally:
        rabbit_send('unregister', f'NODE_{str(NODE_NAME)}')

        
