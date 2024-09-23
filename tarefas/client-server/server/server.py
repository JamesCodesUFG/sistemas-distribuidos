import socket
import threading

BUFFER_SIZE = 4096

def server():
    server_address = ('localhost', 8080)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(server_address)

    server.listen(1)

    while True:
        client, address = server.accept()

        client_thread = threading.Thread(target=handle_client, args=(client, address))
        client_thread.start()

def handle_client(client, client_address):
    message = decode_request(client.recv(BUFFER_SIZE))

    print(message)

    match message[0]:
        case 'GET':
            handle_get(client, message[1])
        case 'POST':
            handle_post(client, message[1], int(message[2]))

def decode_request(data: bytes):
    message = data.decode('utf-8')

    return message.split('$')

def handle_get(client, file_name):
    try:
        file = open(file_name + '.txt', 'r', encoding='utf-8')

        message = file.read().encode()

        message_size = len(message)

        client.send(f'OK${len(message)}'.encode())

        for inner in range(0, int(message_size / BUFFER_SIZE) + 1):
            client.send(message[inner * BUFFER_SIZE: (inner + 1) * BUFFER_SIZE])

    except FileNotFoundError as fileNotFound:
        message = 'ERROR$FILE_NOT_FOUND'.encode()

        client.send(message)
    finally:
        client.close()

def handle_post(client, file_name, size):
    data = b''

    while len(data) < size:
        data = data + client.recv(BUFFER_SIZE)

    save_file(file_name, data)

def save_file(file_name: str, data: bytes):
    file_data = data.decode()

    file = open(file_name + '.txt', 'w', encoding='utf-8')

    file.write(file_data)

server()

