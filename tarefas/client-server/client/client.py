import time
import socket

BUFFER_SIZE = 4096

def client(flag, file_name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('localhost', 8080))

    match flag:
        case 'GET':
            print('Usúario ira realizar um GET...')
            handle_get(client, file_name)
        case 'POST':
            print('Usúario ira realizar um POST...')
            handle_post(client, file_name)

def handle_get(client: socket, file_name: str):
    print('GET enviado ao servidor...')
    message = f'GET${file_name}'.encode()

    client.send(message)

    response = decode_response(client.recv(BUFFER_SIZE))
    print(f'Resposta recebida: {response}')

    match response[0]:
        case 'OK':
            data = b''

            data_size = int(response[1])

            while len(data) < data_size:
                data = data + client.recv(BUFFER_SIZE)

            save_file(file_name, data)

        case 'ERROR':
            handle_error(response[1])

    client.close()

def save_file(file_name: str, data: bytes):
    file_data = data.decode()

    file = open(file_name + '.txt', 'w', encoding='utf-8')

    file.write(file_data)

def handle_post(client: socket, file_name: str):
    try:
        file = open(file_name + '.txt', 'r', encoding='utf-8')

        data = file.read().encode()

        data_size = len(data)

        message = f'POST${file_name}${data_size}'.encode()

        client.send(message)

        for inner in range(0, int(data_size / BUFFER_SIZE) + 1):
            client.send(data[inner * BUFFER_SIZE : (inner + 1) * BUFFER_SIZE])

    except FileNotFoundError as fileNotFound:
        print('Nome do arquivo não encontrado...')

    finally:
        client.close()

def handle_error(error_msg: str):
    match error_msg:
        case 'FILE_NOT_FOUND':
            print('Nome do arquivo não foi encontrado.')

def decode_response(data: bytes):
    response = data.decode()

    return response.split('$')

client('GET', 'alice')