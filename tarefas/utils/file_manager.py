import os
import sys
import shutil

class FileManager:
    def __init__(self, path: str):
        self.path = self.__file_dir() + f'/{path}'

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def read(self, name: str) -> bytes:
        data: bytes = None

        with open(f'{self.path}/{name}', 'rb') as file:
            data = file.read()

        return data

    def write(self, name: str, data: bytes) -> None:
        if os.path.exists(name):
            return

        with open(f'{self.path}/{name}', 'wb') as file:
            file.write(data)

    def delete(self, file_name: str):
        try:
            os.remove(f'{self.path}/{file_name}')
        except Exception as exception:
            raise exception
        
    def list(self) -> list[str]:
        itens = os.listdir(self.path)
        
        arquivos = [item for item in itens if os.path.isfile(os.path.join(self.path, item))]

        return arquivos
    
    def exit(self):
        shutil.rmtree(self.path)

    def __file_dir(self) -> str:
        main_file = os.path.dirname(os.path.abspath(sys.argv[0]))

        return main_file