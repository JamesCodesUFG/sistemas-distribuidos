import client
from valk import Valk
from pessoa import *
from pprint import pprint

PESSOA_A = Pessoa('Tiago Goncalves Maia Geraldine', Endereco('R 16', 'Vila Itatiaia', 7), DadosBancarios('Banco do Brasil', '1234', '00012345'))
PESSOA_B = Pessoa('Vitor di Lorenzzi Nunes da Cunha', Endereco('28A', 'Setor Aeroporto', 295), DadosBancarios('Banco do Brasil', '5678', '00067891'))
PESSOA_C = Pessoa('Lucas Goncalves Maia Geraldine', Endereco('R 16', 'Vila Itatiaia', 7), DadosBancarios('Banco do Brasil', '1357', '00013579'))

def exemplo_post(pessoa: Pessoa):
    pessoa_as_valk = pessoa.to_valk()

    valk_as_bytes = Valk.encode(pessoa_as_valk)

    client.post(valk_as_bytes)

def exemplo_get():
    response = client.get()

    pessoas_as_valk = Valk.decode(response)

    for inner in range(0, len(pessoas_as_valk)):
        pprint(vars(Pessoa.from_valk(pessoas_as_valk[inner])))
        print('\n\n')

for inner in range(0, 8):
    exemplo_post(PESSOA_A)
    exemplo_post(PESSOA_B)
    exemplo_post(PESSOA_C)
    exemplo_get()
