from enum import Enum

class Flag(Enum):
    LONG = 0
    CHAR = 1

class Valk:
    def encode(data: list[tuple]) -> bytes:
        result = b''

        for inner in range(0, len(data)):
            attr = data[inner]

            match attr[0]:
                case Flag.LONG:
                    bytes_data = attr[1].to_bytes(4, 'little', signed=True)
                    bytes_flag = (-1).to_bytes(1, 'little', signed=True)

                    result = result + bytes_flag + bytes_data
                case Flag.CHAR:
                    byte_data = attr[1].encode()
                    byte_flag = len(byte_data).to_bytes(1, 'little', signed=True)

                    result = result + byte_flag + byte_data

        return result

    def decode(data: bytes) -> list[list[(tuple)]]:
        result: list[list[(tuple)]] = []

        index = 0
        bytes_read = 0

        while bytes_read != len(data):
            result.append([])

            attr_read = 0

            while attr_read != 6:
                flag: int = data[bytes_read]

                match Flag(bin(flag)[2]):
                    case Flag.LONG:
                        result[index].append((Flag.LONG, data[bytes_read + 1: bytes_read + 5]))
                        bytes_read = bytes_read + 4
                    case Flag.CHAR:
                        result[index].append((Flag.CHAR, data[bytes_read + 1: bytes_read + flag + 1]))
                        bytes_read = bytes_read + flag

                attr_read = attr_read + 1
                bytes_read = bytes_read + 1
                

            