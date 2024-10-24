#REDIS para fazer cache, implementar
#COntainer implementar;

from enum import Enum
import sys


BUFFER_SIZE = 60000

class RequestMethod(Enum):
    GET = 1
    LIST = 2
    POST = 3
    DELETE = 4

# 10*: Confirmação de sucesso.
# 20*: Houve um erro com a requisição.
# 30*: Houve um erro com o sistama.
class ResponseCode(Enum):
    OK = 100
    READY = 101
    SUCCESS = 200
    ERROR = 300
    NOT_FOUND = 301
    BAD_REQUEST = 302
    SERVICE_UNAVAILABLE = 401

class Request:
    def __init__(self, method: RequestMethod, path: str, lenght: int = 0):
        self.method = method
        self.path = path
        self.lenght = lenght

        sys.set_int_max_str_digits(10000000)

    @staticmethod
    def decode(data: bytes) -> 'Request':
        path_end = int.from_bytes(data[1: 3]) + 3
        return Request(RequestMethod(data[0]), data[3:path_end].decode(), int.from_bytes(data[path_end:]))

    def encode(self) -> bytes:
        return self.method.value.to_bytes(1) + len(self.path).to_bytes(2) + self.path.encode() + self.lenght.to_bytes(4)
    
    def __str__(self) -> str:
        return f'{self.method.name} {self.path} {self.lenght}'

class Response:
    def __init__(self, status: ResponseCode, lenght: int = 0):
        self.status = status
        self.lenght = lenght

    @staticmethod
    def decode(data: bytes) -> 'Response':
        return Response(ResponseCode(data[0]), int.from_bytes(data[1:5]))

    def encode(self) -> bytes:
        return self.status.value.to_bytes(1) + self.lenght.to_bytes(4)

    def __str__(self) -> str:
        return f'{self.status.name} {self.lenght}'