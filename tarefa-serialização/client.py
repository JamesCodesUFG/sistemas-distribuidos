from enum import Enum

import socket

BUFFER_SIZE = 128

SERVER_ADDRESS = ('192.168.6.149', 27015)

class Flag(Enum):
    LONG = 0
    CHAR = 1

class Endereco:
    def __init__(self, rua: str, bairro: str, numero: int):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero

    @staticmethod
    def from_valk():
        pass
    
    def to_valk(self) -> bytes:
        rua_as_valk = to_valk(Flag.CHAR, self.rua)
        bairro_as_valk = to_valk(Flag.CHAR, self.bairro)
        numero_as_valk = to_valk(Flag.LONG, self.numero)

        return rua_as_valk + bairro_as_valk + numero_as_valk

class DadosBancarios:
    def __init__(self, banco: str, agencia: str, conta: str):
        self.banco = banco
        self.agencia = agencia
        self.conta = conta

    @staticmethod
    def from_valk():
        pass

    def to_valk(self) -> bytes:
        banco_as_valk = to_valk(Flag.CHAR, self.banco)
        agencia_as_valk = to_valk(Flag.CHAR, self.agencia)
        conta_as_valk = to_valk(Flag.CHAR, self.conta)

        return banco_as_valk + agencia_as_valk + conta_as_valk

class Pessoa:
    def __init__(self, nome: str, endereco: Endereco, dados_bancarios: DadosBancarios):
        self.nome = nome
        self.endereco = endereco
        self.dados_bancarios = dados_bancarios

    @staticmethod
    def from_valk():
        pass

    def to_valk(self) -> bytes:
        nome_as_valk = to_valk(Flag.CHAR, self.nome)
        endereco_as_valk = self.endereco.to_valk()
        dados_bancarios_as_valk = self.dados_bancarios.to_valk()

        return nome_as_valk + endereco_as_valk + dados_bancarios_as_valk
    
def to_valk(flag: Flag, data: str | int) -> bytes:
    match flag:
        case Flag.LONG:
            byte_data = data.to_bytes(4, 'big', signed=True)
            byte_flag = (-1).to_bytes(1, 'big', signed=True)

            return byte_flag + byte_data
        case Flag.CHAR:
            byte_data = data.encode()
            byte_flag = len(byte_data).to_bytes(1, 'big', signed=True)
            
            return byte_flag + byte_data

def from_valk(data: bytes) -> list[str]:
    result: list[str] = []

    bytes_read = 0

    while bytes_read != len(data):
        string_size = data[bytes_read]

        result.append(data[bytes_read + 1 : bytes_read + string_size + 1].decode())

        bytes_read = bytes_read + string_size + 1

    return result

def create_socket():
    server_address = (SERVER_ADDRESS)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(server_address)

    return client

def get():
    client = create_socket()

    client.send('GET'.encode())

    data = b''

    while True:
        response = client.recv(BUFFER_SIZE)

        if response != b'':
            data = data + response
        else:
            break

    print(from_valk(data))

    client.close()

def post(data: Pessoa):
    client = create_socket()

    client.send('POST'.encode())

    payload = data.to_valk()

    for inner in range(0, len(payload), BUFFER_SIZE):
        client.send(payload[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    client.close()

#__endereco = Endereco('Rua R16', 'Vila Itatiaia', 7)

#__dados_bancarios = DadosBancarios('Banco do Brasil', '09-8976', '54326')

#__pessoa = Pessoa('Tiago Goncalves Maia Geraldine', __endereco, __dados_bancarios)