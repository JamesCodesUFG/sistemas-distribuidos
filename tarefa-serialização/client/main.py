import client
from valk import Valk
from pessoa import *
from pprint import pprint

def exemplo_post():
    endereco = Endereco('Rua R 16', 'Vila Itatiaia', 7)
    dados_bancarios = DadosBancarios('Banco do Brasil', '1234', '00012345')
    pessoa = Pessoa('Tiago Gonçalves Maia Geraldine', endereco, dados_bancarios)

    pessoa_as_valk = pessoa.to_valk()

    valk_as_bytes = Valk.encode(pessoa_as_valk)

    client.post(valk_as_bytes)

def exemplo_get():
    response = client.get()

    pessoas_as_valk = Valk.decode(response)

    for inner in range(0, len(pessoas_as_valk)):
        pprint(vars(Pessoa.from_valk(pessoas_as_valk[0])))

exemplo_post()
