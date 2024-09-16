from enum import Enum

class FlagType(Enum):
    LONG = 1
    CHAR = 0

class Valk:
    @staticmethod
    def encode(data: list[tuple]) -> bytes:
        result = b''

        for inner in range(0, len(data)):
            match data[inner][0]:
                case FlagType.LONG:
                    byte_data = data[inner][1].to_bytes(4, 'little', signed=True)
                    byte_flag = __encode_flag__(data[inner][0])
                case FlagType.CHAR:
                    byte_data = data[inner][1].encode()
                    byte_flag = __encode_flag__(data[inner][0], len(data[inner][1])) 

            result = result + byte_flag + byte_data

        return result

    @staticmethod
    def decode(data: bytes) -> list[list[(tuple)]]:
        result: list[list[(tuple)]] = []

        bytes_read = 0

        while bytes_read != len(data):
            new_pessoa = []

            for inner in range(0, 7):
                flag, data_size = __decode_flag__(data[bytes_read])

                bytes_read = bytes_read + 1

                match flag:
                    case FlagType.LONG:
                        new_pessoa.append((FlagType.LONG, data[bytes_read: bytes_read + 4]))
                        bytes_read = bytes_read + 4
                    case FlagType.CHAR:
                        new_pessoa.append((FlagType.CHAR, data[bytes_read: bytes_read + data_size].decode()))
                        bytes_read = bytes_read + data_size

            result.append(new_pessoa)
            
        return result
    
def __encode_flag__(flag: FlagType, size: int = 4) -> bytes:
    return ((flag.value << 7) + size).to_bytes(1, 'little')

def __decode_flag__(flag: int) -> tuple:
    return (FlagType(flag >> 7), flag & 0b01111111)
            