from enum import Enum

BUFFER_SIZE = 1028

class MyProtocol(Enum):
    DOWNLOAD = 1
    UPLOAD = 2
    SEARCH = 3