from enum import Enum

import socket

class Command(Enum):
    DOWNLOAD = 1
    UPLOAD = 2
    SEARCH = 3
    HELP = 4

def client(command: Command):
    server_addres = ('localhost', 8080)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(server_addres)

    client.send('Hello World'.encode('utf-8'))

    client.close()

def download(client: socket):
    pass

def upload(client: socket):
    pass


def get_user_command() -> int:
    client_input = input('\n> ').split(' ')

    command = client_input[0]

    match command:
        case 'download':
            pass
        case 'upload':
            pass
        case 'search':
            pass
        case 'help':
            pass

    return int(command)

def print_help():
    print('dowanload (image_name)   - Baixa a imagem com nome selecionado.')
    print('upload (dir/image)       - Envia a imagem no diretório selecionado.')
    print('search                   - Retorna uma lista com todas as imagens disponiveis.')

client(Command.DOWNLOAD)