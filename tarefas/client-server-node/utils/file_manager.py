import os

class FileManager:
    def __init__(self, path: str):
        self.path = path

    def read(self, file_name: str) -> bytes:
        data: bytes = None

        with open(f'{self.path}/{file_name}', 'rb') as file:
            data = file.read()

        return data

    def write(self, file_name: str, data: bytes) -> None:
        with open(f'{self.path}/{file_name}', 'wb') as file:
            file.write(data)

    def delete(self, file_name: str):
        try:
            os.remove(f'{self.path}/{file_name}')
        except Exception as exception:
            raise exception
