from enum import Enum

class Flag(Enum):
    LONG = 1
    CHAR = 0

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

        while bytes_read + 1 != len(data):
            result.append([])

            for inner in range(0, 7):
                flag: int = data[bytes_read]

                flag_type = (flag & 0b10000000) >> 7

                bytes_read = bytes_read + 1

                match Flag(flag_type):
                    case Flag.LONG:
                        result[index].append((Flag.LONG, data[bytes_read: bytes_read + 4]))
                        bytes_read = bytes_read + 4
                    case Flag.CHAR:
                        result[index].append((Flag.CHAR, data[bytes_read: bytes_read + flag].decode()))
                        bytes_read = bytes_read + flag

            index = index + 1
            

        return result
                
                

            