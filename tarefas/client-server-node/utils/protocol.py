#REDIS para fazer cache, implementar
#COntainer implementar;

from enum import Enum

BUFFER_SIZE = 16384

class RequestMethod(Enum):
    GET = 1
    POST = 2
    DELETE = 3

# 10*: Confirmação de sucesso.
# 20*: Houve um erro com a requisição.
# 30*: Houve um erro com o sistama.
class ResponseCode(Enum):
    OK = 100
    READY = 101
    NOT_FOUND = 201
    BAD_REQUEST = 202
    SERVICE_UNAVAILABLE = 301

class Request:
    def __init__(self, method: RequestMethod, path: str, lenght: int = 0):
        self.method = method
        self.path = path
        self.lenght = lenght

    @staticmethod
    def decode(data: bytes) -> 'Request':
        path_end = int.from_bytes(data[1: 3]) + 3
        return Request(RequestMethod(data[0]), data[3:path_end].decode(), int.from_bytes(data[path_end:]))

    def encode(self) -> bytes:
        return self.method.value.to_bytes(1) + len(self.path).to_bytes(2) + self.path.encode() + self.lenght.to_bytes(4)

class Response:
    def __init__(self, status: ResponseCode, lenght: int = 0):
        self.status = status
        self.lenght = lenght

    @staticmethod
    def decode(data: bytes) -> 'Response':
        return Response(ResponseCode(data[0]), int.from_bytes(data[1:5]))

    def encode(self) -> bytes:
        return self.status.value.to_bytes(1) + self.lenght.to_bytes(4)

