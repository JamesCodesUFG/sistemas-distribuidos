import socket

from valk import Flag, Valk

BUFFER_SIZE = 128

SERVER_ADDRESS = ('192.168.6.149', 27015)

class Endereco:
    def __init__(self, rua: str, bairro: str, numero: int):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero

    @staticmethod
    def from_valk():
        pass
    
    def to_valk(self) -> bytes:
        return [(Flag.CHAR, self.rua), (Flag.CHAR, self.bairro), (Flag.LONG, self.numero)]

class DadosBancarios:
    def __init__(self, banco: str, agencia: str, conta: str):
        self.banco = banco
        self.agencia = agencia
        self.conta = conta

    @staticmethod
    def from_valk():
        pass

    def to_valk(self) -> bytes:
        return [(Flag.CHAR, self.banco), (Flag.CHAR, self.agencia), (Flag.CHAR, self.conta)]

class Pessoa:
    def __init__(self, nome: str, endereco: Endereco, dados_bancarios: DadosBancarios):
        self.nome = nome
        self.endereco = endereco
        self.dados_bancarios = dados_bancarios

    @staticmethod
    def from_valk():
        pass

    def to_valk(self) -> bytes:
        return [(Flag.CHAR, self.nome), *self.endereco.to_valk(), *self.dados_bancarios.to_valk()]

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