from enum import Enum

BUFFER_SIZE = 128

class Protocol(Enum):
    GET: 1
    LIST: 2
    POST: 3
    DELETE: 4

class Request:
    pass

class Response:
    def __init__(self, data: bytes):
        pass

    def __decode_data(data):
        pass

