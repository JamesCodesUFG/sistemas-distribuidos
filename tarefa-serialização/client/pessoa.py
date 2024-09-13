from valk import FlagType

class Endereco:
    def __init__(self, rua: str, bairro: str, numero: int):
        self.rua = rua
        self.bairro = bairro
        self.numero = numero

    @staticmethod
    def from_valk(data: list[tuple]) -> "Endereco":
        return Endereco(data[0][1], data[1][1], data[2][1])
    
    def to_valk(self) -> bytes:
        return [(FlagType.CHAR, self.rua), (FlagType.CHAR, self.bairro), (FlagType.LONG, self.numero)]

class DadosBancarios:
    def __init__(self, banco: str, agencia: str, conta: str):
        self.banco = banco
        self.agencia = agencia
        self.conta = conta

    @staticmethod
    def from_valk(data: list[tuple]) -> "DadosBancarios":
        return DadosBancarios(data[0][1], data[1][1], data[2][1])

    def to_valk(self) -> bytes:
        return [(FlagType.CHAR, self.banco), (FlagType.CHAR, self.agencia), (FlagType.CHAR, self.conta)]

class Pessoa:
    def __init__(self, nome: str, endereco: Endereco, dados_bancarios: DadosBancarios):
        self.nome = nome
        self.endereco = endereco
        self.dados_bancarios = dados_bancarios

    @staticmethod
    def from_valk(data: list[tuple]) -> "Pessoa":
        return Pessoa(data[0][1], Endereco.from_valk(data[1:4]), DadosBancarios.from_valk(data[4:8]))

    def to_valk(self) -> bytes:
        return [(FlagType.CHAR, self.nome), *self.endereco.to_valk(), *self.dados_bancarios.to_valk()]