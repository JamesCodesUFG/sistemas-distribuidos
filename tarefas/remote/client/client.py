import rpyc

from utils.file_manager import FileManager
from utils.input_manager import InputManager, Commmand

class Client:
    __file_manager: FileManager = FileManager('images')

    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.flag = True
        self.__host = host
        self.__port = port

        self.__geoeye = rpyc.connect(self.__host, self.__port)

        self.__input = InputManager({
            'get': Commmand(exec=self.get, has_args=True),
            'post': Commmand(exec=self.post, has_args=True),
            'list': Commmand(exec=self.list, has_args=False),
            'delete': Commmand(exec=self.delete, has_args=True),
            'exit': Commmand(exec=self.exit, has_args=False)
        })

        self.loop()

    def loop(self) -> None:
        while self.flag:
            self.__input.next()

    def get(self, name: str) -> None:
        file = self.__connect().get(name)

        self.__file_manager.write(name, file)

    def post(self, name: str) -> None:
        file = self.__file_manager.read(name)

        self.__connect().post(name, file)

    def list(self) -> None:
        names = self.__connect().list()

        print(f'\n{names}\n')

    def delete(self, name: str) -> None:
        self.__connect().delete(name)
    
    def exit(self):
        self.flag = False
    
    def __connect(self):
        try:
            self.__geoeye.ping()
        except:
            print(f'\n[WARNING] Restabelecendo conexão com servidor...\n')

            self.__geoeye = rpyc.connect(self.__host, self.__port)
        finally:
            return self.__geoeye.root
    
Client()