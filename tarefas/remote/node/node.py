import sys
import rpyc
import uuid

from rpyc.utils.server import ThreadedServer

from utils.rabbit import *
from utils.file_manager import FileManager

NODE_NAME = f'NODE_{sys.argv[2]}'

fmanager: FileManager = FileManager(f'{NODE_NAME}_{uuid.uuid4()}')

def post(data: dict):
    global fmanager

    fmanager.write(data['name'], data['file'])


def delete(data: dict):
    global fmanager

    fmanager.delete(data['name'])

rabbit_post = RabbitMultipleReceiver(f'post_{NODE_NAME}', post).start()
rabbit_delete = RabbitMultipleReceiver(f'delete_{NODE_NAME}', delete).start()

class NodeService(rpyc.Service):
    ALIASES = [NODE_NAME]

    def exposed_get(self, name: str) -> bytes:
        global fmanager

        file = fmanager.read(name)

        return file
    
    def exposed_sync(self) -> None:
        global fmanager

        files_names = fmanager.list()

        for file_name in files_names:
            file = fmanager.read(file_name)

            rabbit_multiple_send(f'post_{NODE_NAME}', {
                'name': file_name,
                'file': file
            })


if __name__ == "__main__":
    import monitor

    __hdd_monitor = monitor.HDDMonitor(0.95, NODE_NAME)

    try:
        __hdd_monitor.start()

        server = ThreadedServer(NodeService, auto_register=True, protocol_config={
            'sync_request_timeout': 600,
            'allow_all_attrs': True,
            'allow_pickle': True,
            'max_message_size': 10*9,
        })

        rabbit_single_send('register', { 'name': NODE_NAME })

        print(f'\nNó iniciado em {(server.host, server.port)}\n')

        server.start()
    except:
        __hdd_monitor.stop()
    finally:
        rabbit_single_send('unregister', { 'name': NODE_NAME })

        
