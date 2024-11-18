import rpyc

from utils.file_manager import FileManager

class Client:
    __file_manager: FileManager = FileManager('images')

    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.geo_eye = rpyc.connect(host, port).root

        self.loop()

    def loop(self) -> None:
        while True:
            _input = self.input()

            match (_input[0]):
                case 'get':
                    self.get(_input[1])
                case 'post':
                    self.post(_input[1])
                case 'list':
                    self.list()
                case 'delete':
                    self.delete(_input[1])

    def get(self, name: str) -> None:
        file = self.geo_eye.get(name)

        self.__file_manager.write(name, file)

    def post(self, name: str) -> None:
        file = self.__file_manager.read(name)

        self.geo_eye.post(name, file)

    def list(self) -> None:
        names = self.geo_eye.list()

        print(f'{names}\n')

    def delete(self, name: str) -> None:
        self.geo_eye.delete(name)

    def input(self) -> tuple:
        input_data = input('> ')

        input_list = input_data.split(' ')

        return (input_list[0], input_list[1] if input_list[0] != 'list' else '')
    
Client()