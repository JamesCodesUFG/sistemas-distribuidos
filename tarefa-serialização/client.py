from enum import Enum

import socket

class Valkiria(Enum):
    GET = 0
    POST = 1

class Flag(Enum):
    LONG = False
    CHAR = True

class DataBase:
    def __init__(self, banco: str, agencia: str, conta: str):
        self.banco = banco
        self.agencia = agencia
        self.conta = conta

class Endereco:
    def __init__(self, rua: str, bairro: str, numero: int):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero

class Pessoa:
    def __init__(self, nome: str, endereco: Endereco, data_base: DataBase):
        self.nome = nome
        self.endereco = endereco
        self.data_base = data_base

    def to_valkiria(self) -> bytes:
        return (-len(self.nome).to_bytes(2, 'big')[3]) + 
    
def calc_valkiria(flag: Flag, data: str | int):
    

    return 

def client():
    server_address = ('192.168.6.149', 27015)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(server_address)

    client.send('Tiago'.encode('utf-8'))

    for inner in range(0, 2):
        data = client.recv(1024)

        print(data)

    client.close()

client()